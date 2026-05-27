"""Classify a Sacramento building permit row into a standardised category string.

Rules are applied in priority order; the first match wins.  See
docs/classification-strategy.md for rationale and edge-case notes.
"""
from __future__ import annotations

CATEGORIES = frozenset({
    "new_construction_residential",
    "new_construction_commercial",
    "addition",
    "remodel_residential",
    "remodel_commercial",
    "adu",
    "demolition",
    "solar",
    "roofing",
    "mechanical",
    "electrical",
    "plumbing",
    "other",
})

# ── Coded Sub_Type sets ────────────────────────────────────────────────────────

_DEMOLITION_SUBTYPES = frozenset({
    "Demolition", "Demolition Interior", "Housing-Demo",
})
_NEW_CONSTRUCTION_RES_SUBTYPES = frozenset({
    # Unit-count codes for multi-family residential new construction
    "1-5", "5+", "Production Permit",
})
_REMODEL_SUBTYPES = frozenset({
    "Remodel", "Minor", "Web-Minor",
    "Housing-Minor", "Housing-Rental Program-Minor", "Housing-Rental Program",
    "Housing Dept Permit", "Phased",
})

# ── Category-field sets (used for some mechanical/electrical signals) ──────────

_HVAC_CATEGORIES = frozenset({"HVAC"})
_ELECTRICAL_CATEGORIES = frozenset({
    "Electric", "Electrical", "EV Charging Station", "EV Station Electrical",
})

# ── Work_Desc keyword tuples (matched on lowercased description) ───────────────

_ADU_KWS = ("adu", "accessory dwelling", "accessory unit", "junior adu", "jadu")
_SOLAR_KWS = ("solar", " pv ", "pv system", "photovoltaic", "battery storage")
# "tear off" and "squares" are the most reliable roofing signals in SAC data
_ROOFING_KWS = ("tear off", "re-roof", "reroof", "shingle", "squares of", "roof")
_ELECTRICAL_KWS = (
    "electrical permit",
    "panel change",
    "panel upgrade",
    "ev charger",
    "electric vehicle",
    "service upgrade",
    "amp panel",
    "amp service",
)
_MECHANICAL_KWS = (
    "hvac",
    "furnace",
    "boiler",
    "heat pump",
    "split system",
    "air handler",
    "air condition",
    "duct",
)
_PLUMBING_KWS = (
    "plumbing permit",
    "plumb",
    "water service",
    "water heater",
    "sewer",
    "drain line",
    "pipe replacement",
)


# ── Classifier ─────────────────────────────────────────────────────────────────

def classify_permit(row) -> str:
    """Return a category string for *row* (a dict-like with permit attributes).

    Always returns a value in CATEGORIES.
    """
    sub = str(row.get("Sub_Type") or "").strip()
    type_ = str(row.get("Type") or "").strip()
    cat = str(row.get("Category") or "").strip()
    desc = str(row.get("Work_Desc") or "").lower()

    # 1. Demolition — clean coded signal, check first
    if sub in _DEMOLITION_SUBTYPES:
        return "demolition"

    # 2. ADU — keyword check before new-construction/addition because ADU permits
    #    are filed under both New Building and Addition sub-types
    if any(kw in desc for kw in _ADU_KWS):
        return "adu"

    # 3–4. New construction
    if sub == "New Building":
        return (
            "new_construction_residential"
            if type_ == "Residential"
            else "new_construction_commercial"
        )
    if sub in _NEW_CONSTRUCTION_RES_SUBTYPES:
        return "new_construction_residential"

    # 5. Addition
    if sub == "Addition":
        return "addition"

    # 6. Solar — checked before roofing: "roof-mount solar PV" must be solar
    if any(kw in desc for kw in _SOLAR_KWS):
        return "solar"

    # 7. Roofing
    if any(kw in desc for kw in _ROOFING_KWS):
        return "roofing"

    # 8. Electrical — checked before mechanical; "panel change-out" is electrical
    if cat in _ELECTRICAL_CATEGORIES or any(kw in desc for kw in _ELECTRICAL_KWS):
        return "electrical"

    # 9. Mechanical (HVAC)
    if cat in _HVAC_CATEGORIES or any(kw in desc for kw in _MECHANICAL_KWS):
        return "mechanical"

    # 10. Plumbing
    if any(kw in desc for kw in _PLUMBING_KWS):
        return "plumbing"

    # 11. Generic remodel — catches Minor/Web-Minor permits not caught above
    if sub in _REMODEL_SUBTYPES:
        return (
            "remodel_residential" if type_ == "Residential" else "remodel_commercial"
        )

    return "other"
