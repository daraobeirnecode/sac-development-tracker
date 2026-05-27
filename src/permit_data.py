"""Fetch Sacramento building permit data from ArcGIS Hub, cache as Parquet.

Public API
----------
    fetch_issued_permits(year_filter=None, fresh=False)  -> gpd.GeoDataFrame
    fetch_applied_permits(year_filter=None, fresh=False) -> gpd.GeoDataFrame

Both return a GeoDataFrame with SCHEMA_COLUMNS plus a 'category' column
(from classifier.py), Status_Date parsed to pd.Timestamp, Valuation as float
(zero treated as unreported → NaN), and geometry in EPSG:4326.

Date-field note
---------------
Status_Date is typed String in all four ArcGIS services (esriFieldTypeString),
arriving as "MM/DD/YYYY" strings.  This contradicts the CLAUDE.md statement
that ArcGIS date fields come back as epoch milliseconds — that would apply only
to fields typed esriFieldTypeDate.  See docs/permit-schemas.md for the actual
field types.

Geometry note
-------------
These FeatureServer endpoints may carry null geometry for all records (no
spatial component on the service).  returnGeometry=true is requested; null
geometries are stored as None and preserved through the Parquet cache.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import Point

# ── Schema ─────────────────────────────────────────────────────────────────────

SCHEMA_COLUMNS = (
    "OBJECTID", "Type", "Sub_Type", "Category", "Application",
    "Rpt_Status", "Status_Date", "Current_Status", "Parcel_No",
    "Address", "Site_Location", "ZIP", "Inspection_District",
    "House_Count", "Project_Sq_Ft", "Habitable_Sq_Ft", "Valuation",
    "Activity_Code", "Contractor", "Council_Dist", "Comm_Plan_Area",
    "Work_Desc", "Project_Name",
)

# ── Constants ──────────────────────────────────────────────────────────────────

ENDPOINTS: dict[str, str] = {
    "issued_current": (
        "https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services"
        "/BldgPermitIssued_CurrentYear/FeatureServer/0"
    ),
    "issued_archive": (
        "https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services"
        "/BldgPermitIssued_Archive/FeatureServer/0"
    ),
    "applied_current": (
        "https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services"
        "/BldgPermitApplied_CurrentYear/FeatureServer/0"
    ),
    "applied_archive": (
        "https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services"
        "/BldgPermitApplied_Archive/FeatureServer/0"
    ),
}

# Resolved relative to this file so it works when imported from a sibling repo
CACHE_DIR: Path = Path(__file__).parent.parent / "data" / "cache"
PAGE_SIZE: int = 2000
CACHE_TTL: timedelta = timedelta(hours=24)
# Cache uses GPKG (via pyogrio) — pyarrow is not in the declared stack.
# Switch to .parquet by installing pyarrow and swapping _cache_path + _load_dataset.


# ── Cache helpers ──────────────────────────────────────────────────────────────

def _cache_path(dataset: str) -> Path:
    return CACHE_DIR / f"{dataset}.gpkg"


def _is_fresh(path: Path) -> bool:
    if not path.exists():
        return False
    age = datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)
    return age < CACHE_TTL


# ── Fetch ──────────────────────────────────────────────────────────────────────

def _fetch_arcgis(url: str) -> gpd.GeoDataFrame:
    """Paginate an ArcGIS FeatureServer/0 query endpoint.

    Returns a GeoDataFrame in EPSG:4326.  Status_Date and Valuation are NOT yet
    parsed — call _parse_dates and _parse_valuation on the result.
    """
    records: list[dict] = []
    geometries: list[Point | None] = []
    offset = 0

    while True:
        params = {
            "f": "json",
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
            "outSR": "4326",
            "resultOffset": offset,
            "resultRecordCount": PAGE_SIZE,
        }
        resp = requests.get(f"{url}/query", params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"ArcGIS error from {url}: {data['error']}")

        features = data.get("features", [])
        if not features:
            break

        for feat in features:
            records.append(feat["attributes"])
            geom = feat.get("geometry")
            if geom and "x" in geom and geom["x"] is not None:
                geometries.append(Point(geom["x"], geom["y"]))
            else:
                geometries.append(None)

        offset += len(features)
        if len(features) < PAGE_SIZE:
            break

    if not records:
        return gpd.GeoDataFrame(
            columns=list(SCHEMA_COLUMNS) + ["geometry"], crs="EPSG:4326"
        )

    df = pd.DataFrame(records)
    return gpd.GeoDataFrame(df, geometry=geometries, crs="EPSG:4326")


# ── Parsing ────────────────────────────────────────────────────────────────────

def _parse_dates(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Status_Date arrives as "MM/DD/YYYY" strings (esriFieldTypeString in ArcGIS)
    if "Status_Date" in gdf.columns:
        gdf = gdf.copy()
        gdf["Status_Date"] = pd.to_datetime(
            gdf["Status_Date"], format="%m/%d/%Y", errors="coerce"
        )
    return gdf


def _parse_valuation(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Zero valuation means "unreported" for permit types where it doesn't apply
    if "Valuation" in gdf.columns:
        gdf = gdf.copy()
        gdf["Valuation"] = pd.to_numeric(gdf["Valuation"], errors="coerce")
        gdf.loc[gdf["Valuation"] == 0.0, "Valuation"] = float("nan")
    return gdf


# ── Category ───────────────────────────────────────────────────────────────────

def _add_category(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    from .classifier import classify_permit  # lazy import keeps modules decoupled
    gdf = gdf.copy()
    gdf["category"] = gdf.apply(classify_permit, axis=1)
    return gdf


# ── Dataset loader ─────────────────────────────────────────────────────────────

def _load_dataset(name: str, fresh: bool = False) -> gpd.GeoDataFrame:
    """Return parsed GeoDataFrame for *name*, using cache when available."""
    if name not in ENDPOINTS:
        raise ValueError(f"Unknown dataset {name!r}. Valid: {list(ENDPOINTS)}")

    path = _cache_path(name)
    if not fresh and _is_fresh(path):
        return gpd.read_file(path)

    gdf = _fetch_arcgis(ENDPOINTS[name])
    gdf = _parse_dates(gdf)
    gdf = _parse_valuation(gdf)

    path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(path, driver="GPKG")
    return gdf


# ── Public API ─────────────────────────────────────────────────────────────────

def fetch_issued_permits(
    year_filter: int | None = None,
    fresh: bool = False,
) -> gpd.GeoDataFrame:
    """Return issued permits (current year + archive) as a classified GeoDataFrame.

    Parameters
    ----------
    year_filter:
        If given, keep only rows where Status_Date.year == year_filter.
    fresh:
        If True, bypass the cache and re-fetch from the live endpoints.
    """
    current = _load_dataset("issued_current", fresh)
    archive = _load_dataset("issued_archive", fresh)
    merged = pd.concat([current, archive], ignore_index=True)
    gdf = gpd.GeoDataFrame(merged, geometry="geometry", crs="EPSG:4326")
    gdf = _add_category(gdf)
    if year_filter is not None:
        gdf = gdf[gdf["Status_Date"].dt.year == year_filter]
    return gdf


def fetch_applied_permits(
    year_filter: int | None = None,
    fresh: bool = False,
) -> gpd.GeoDataFrame:
    """Return applied permits (current year + archive) as a classified GeoDataFrame.

    Parameters
    ----------
    year_filter:
        If given, keep only rows where Status_Date.year == year_filter.
    fresh:
        If True, bypass the cache and re-fetch from the live endpoints.
    """
    current = _load_dataset("applied_current", fresh)
    archive = _load_dataset("applied_archive", fresh)
    merged = pd.concat([current, archive], ignore_index=True)
    gdf = gpd.GeoDataFrame(merged, geometry="geometry", crs="EPSG:4326")
    gdf = _add_category(gdf)
    if year_filter is not None:
        gdf = gdf[gdf["Status_Date"].dt.year == year_filter]
    return gdf
