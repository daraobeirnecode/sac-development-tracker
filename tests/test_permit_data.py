"""Tests for src/permit_data.py.

All tests are offline — network calls are replaced by a monkeypatched
_fetch_arcgis that returns a minimal in-memory GeoDataFrame.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import pytest

import permit_data as pd_mod
from permit_data import (
    SCHEMA_COLUMNS,
    _parse_dates,
    _parse_valuation,
)


# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_gdf(n: int = 3) -> gpd.GeoDataFrame:
    """Minimal GeoDataFrame that satisfies SCHEMA_COLUMNS."""
    data: dict = {col: [None] * n for col in SCHEMA_COLUMNS}
    # Build a Valuation list of length n: first=5000, second=0, rest=None
    valuation = ([5000.0] + [0.0] + [None] * (n - 2))[:n] if n >= 2 else [5000.0] * n
    data.update(
        OBJECTID=list(range(n)),
        Type=["Residential"] * n,
        Sub_Type=["Minor"] * n,
        Category=["Single Family"] * n,
        Application=[f"RES-260000{i}" for i in range(n)],
        Status_Date=["01/15/2026"] * n,
        Work_Desc=["Bathroom remodel"] * n,
        Valuation=valuation,
    )
    return gpd.GeoDataFrame(data, geometry=[None] * n, crs="EPSG:4326")


# ── Date parsing ───────────────────────────────────────────────────────────────

def test_date_parsing_string():
    gdf = _make_gdf()
    result = _parse_dates(gdf)
    assert result["Status_Date"].iloc[0] == pd.Timestamp("2026-01-15")


def test_date_parsing_null_becomes_nat():
    gdf = _make_gdf(2)
    gdf = gdf.copy()
    gdf["Status_Date"] = [None, "01/15/2026"]
    result = _parse_dates(gdf)
    assert pd.isna(result["Status_Date"].iloc[0])
    assert result["Status_Date"].iloc[1] == pd.Timestamp("2026-01-15")


# ── Valuation parsing ──────────────────────────────────────────────────────────

def test_valuation_zero_becomes_nan():
    gdf = _make_gdf()
    result = _parse_valuation(gdf)
    assert pd.isna(result["Valuation"].iloc[1])  # was 0.0


def test_valuation_nonzero_preserved():
    gdf = _make_gdf()
    result = _parse_valuation(gdf)
    assert result["Valuation"].iloc[0] == 5000.0


def test_valuation_null_preserved_as_nan():
    gdf = _make_gdf()
    result = _parse_valuation(gdf)
    assert pd.isna(result["Valuation"].iloc[2])  # was None


# ── Schema validation ──────────────────────────────────────────────────────────

def test_required_columns_issued(tmp_path, monkeypatch):
    monkeypatch.setattr(pd_mod, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(pd_mod, "_fetch_arcgis", lambda url: _make_gdf(3))
    gdf = pd_mod.fetch_issued_permits(fresh=True)
    assert set(SCHEMA_COLUMNS).issubset(set(gdf.columns))
    assert "category" in gdf.columns


def test_required_columns_applied(tmp_path, monkeypatch):
    monkeypatch.setattr(pd_mod, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(pd_mod, "_fetch_arcgis", lambda url: _make_gdf(3))
    gdf = pd_mod.fetch_applied_permits(fresh=True)
    assert set(SCHEMA_COLUMNS).issubset(set(gdf.columns))
    assert "category" in gdf.columns


# ── Cache behaviour ────────────────────────────────────────────────────────────

def test_cache_hit_skips_fetch(tmp_path, monkeypatch):
    """Cache hit must not call _fetch_arcgis a second time."""
    monkeypatch.setattr(pd_mod, "CACHE_DIR", tmp_path)
    call_count = [0]

    def fake_fetch(url: str) -> gpd.GeoDataFrame:
        call_count[0] += 1
        return _make_gdf(4)

    monkeypatch.setattr(pd_mod, "_fetch_arcgis", fake_fetch)

    # First call: cache miss
    pd_mod._load_dataset("issued_current", fresh=False)
    assert call_count[0] == 1

    # Second call: cache hit — fetch must NOT be called again
    pd_mod._load_dataset("issued_current", fresh=False)
    assert call_count[0] == 1


def test_cache_hit_returns_same_data(tmp_path, monkeypatch):
    """Data returned from cache must match data returned from a fresh fetch."""
    monkeypatch.setattr(pd_mod, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(pd_mod, "_fetch_arcgis", lambda url: _make_gdf(4))

    fresh_result = pd_mod._load_dataset("issued_current", fresh=True)
    cached_result = pd_mod._load_dataset("issued_current", fresh=False)

    assert fresh_result.shape == cached_result.shape
    assert set(fresh_result.columns) == set(cached_result.columns)
    pd.testing.assert_frame_equal(
        fresh_result.drop(columns="geometry").reset_index(drop=True),
        cached_result.drop(columns="geometry").reset_index(drop=True),
        check_dtype=False,
    )
