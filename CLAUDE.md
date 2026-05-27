# Sacramento Development Tracker

## Purpose
A portfolio demo and proto-product that analyzes Sacramento city building
permits to produce monthly development briefs, neighborhood breakdowns,
and an interactive web map. Buyers in mind: real estate brokers,
developers, neighborhood associations, journalists.

## Scope
- Input: Sacramento city ArcGIS Hub permit feeds (issued + applied,
  current + archive).
- Output: monthly Markdown briefs in outputs/briefs/, an interactive web
  map in web/, JSON aggregate stats for reuse.
- Out of scope for now: email watchlists, PDF generation, county-level
  permits (city only), permit prediction or forecasting.

## Behavioral rules
- Build over plan. No long planning documents when working code will do.
- No Docker unless I explicitly ask.
- Accuracy over helpfulness. If a field isn't in the schema, say so —
  don't fabricate. Reference docs/permit-schemas.md as the source of truth.
- Stack is declared: Python 3.10, requests, pandas, geopandas, shapely,
  pyproj, jinja2, folium, pytest. No new dependencies without me asking.
- Small diffs. One concern per commit.
- The scout repo at ~/code/sac-permits-scout is reference material only.
  Do not modify it.

## Domain rules (Dara has 15 years municipal GIS background)
- Coordinate work uses EPSG:4326 (WGS84) for input/output and EPSG:3310
  (California Albers) for any area or distance calculations. Reproject
  explicitly when computing distances.
- Date fields from ArcGIS come back as epoch milliseconds. Convert to
  pd.Timestamp before any analysis.
- Valuation fields are often null or zero on permit types where they
  don't apply. Treat null and zero as "unreported" not as "$0" in
  aggregates.
- The schema doc at docs/permit-schemas.md is the source of truth. If
  you find a discrepancy between the doc and live data, flag it; do not
  silently work around it.

## Safety
- Public open data only. No private credentials needed.
- Cache pulled data to data/cache/ as Parquet. Do not commit cache files.
- No PII transformations — permits are public records but contractor
  names and property owners do appear in some fields. Do not republish
  these in aggregate outputs unless I explicitly say to.

## Verification
- pytest -q from repo root must pass before any commit.
- Cached data freshness: cache TTL is 24h by default, override with
  fresh=True.
- Before any commit: git status shows only intended changes.

## Sibling repo (Workflow C)
A site-intelligence tool lives at ~/code/sac-site-intelligence and will
reuse this repo's permit_data.py and classifier.py in week 3. Keep
those modules clean and importable.
