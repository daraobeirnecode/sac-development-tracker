"""Tests for src/classifier.py.

Hand-classified records are constructed from real Work_Desc patterns observed
in the Sacramento scout sample CSVs (~/code/sac-permits-scout/outputs/).
"""
import pytest
from classifier import CATEGORIES, classify_permit

# ── Hand-classified sample ─────────────────────────────────────────────────────
# Each entry: (permit_row_dict, expected_category)
# Rows cover all 13 categories plus edge cases for keyword-priority ordering.

HAND_CLASSIFIED = [
    # 1. Roofing — "tear off" keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor", "Category": "Single Family",
            "Work_Desc": "E-Permit: Tear Off - Yes, Resheet - No, 23 squares of Composite Class A",
        },
        "roofing",
    ),
    # 2. Electrical — "electrical permit" keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor", "Category": "Single Family",
            "Work_Desc": "Electrical Permit: 125 amp panel change out, like for like",
        },
        "electrical",
    ),
    # 3. Solar — "solar" keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor", "Category": "Single Family",
            "Work_Desc": "6.5kw Solar PV System, 11.5 kw PV Storage System with battery",
        },
        "solar",
    ),
    # 4. Mechanical — "split system" keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor", "Category": "Single Family",
            "Work_Desc": "No Duct Work Permitted. Change-out Split System to Split System",
        },
        "mechanical",
    ),
    # 5. Plumbing — "water heater" keyword
    (
        {
            "Type": "Commercial", "Sub_Type": "Web-Minor", "Category": "Apts 5+",
            "Work_Desc": "Water Heater Permit: Replace gas water heater, like for like",
        },
        "plumbing",
    ),
    # 6. Remodel residential — Minor sub-type, no specific keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Minor", "Category": "Single Family",
            "Work_Desc": "Bathroom Remodel Permit. Interior renovation of existing bathroom",
        },
        "remodel_residential",
    ),
    # 7. Demolition — Sub_Type coded value
    (
        {
            "Type": "Commercial", "Sub_Type": "Demolition", "Category": "Commercial",
            "Work_Desc": "Demolish existing one-story commercial structure",
        },
        "demolition",
    ),
    # 8. New construction residential — New Building + Residential
    (
        {
            "Type": "Residential", "Sub_Type": "New Building", "Category": "Single Family",
            "Work_Desc": "New single family dwelling, 3 bed 2 bath, 1850 sq ft",
        },
        "new_construction_residential",
    ),
    # 9. New construction commercial — New Building + Commercial
    (
        {
            "Type": "Commercial", "Sub_Type": "New Building", "Category": "Office",
            "Work_Desc": "New two-story office building 5000 sq ft",
        },
        "new_construction_commercial",
    ),
    # 10. Addition — Sub_Type coded value, no ADU keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Addition", "Category": "Single Family",
            "Work_Desc": "Room addition 400 sq ft master bedroom and bath",
        },
        "addition",
    ),
    # 11. ADU — keyword beats New Building sub-type (priority check)
    (
        {
            "Type": "Residential", "Sub_Type": "New Building", "Category": "Single Family",
            "Work_Desc": "New ADU 500 sq ft detached unit behind primary residence",
        },
        "adu",
    ),
    # 12. Remodel commercial — Minor sub-type + Commercial type
    (
        {
            "Type": "Commercial", "Sub_Type": "Minor", "Category": "Office",
            "Work_Desc": "Office tenant improvement, reconfigure interior partitions",
        },
        "remodel_commercial",
    ),
    # 13. Solar — "photovoltaic" keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor", "Category": "Single Family",
            "Work_Desc": "Install photovoltaic system 10kw roof mount",
        },
        "solar",
    ),
    # 14. Plumbing — "water service" keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor", "Category": "Single Family",
            "Work_Desc": "Water service replacement or repair, 60 LF",
        },
        "plumbing",
    ),
    # 15. Electrical — Category field signal (EV Charging Station)
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor",
            "Category": "EV Charging Station",
            "Work_Desc": "EV charger installation Level 2, 240V 50A circuit",
        },
        "electrical",
    ),
    # 16. Mechanical — "heat pump" keyword
    (
        {
            "Type": "Residential", "Sub_Type": "Web-Minor", "Category": "Single Family",
            "Work_Desc": "Heat pump installation, replace gas furnace with heat pump",
        },
        "mechanical",
    ),
    # 17. New construction residential — Sub_Type "5+"
    (
        {
            "Type": "Residential", "Sub_Type": "5+", "Category": "Apts 5+",
            "Work_Desc": "New multi-family apartment complex, 20 units",
        },
        "new_construction_residential",
    ),
    # 18. Demolition — "Demolition Interior" Sub_Type
    (
        {
            "Type": "Residential", "Sub_Type": "Demolition Interior",
            "Category": "Single Family",
            "Work_Desc": "Interior demolition prior to full remodel",
        },
        "demolition",
    ),
    # 19. ADU — keyword beats Addition sub-type (priority check)
    (
        {
            "Type": "Residential", "Sub_Type": "Addition", "Category": "Single Family",
            "Work_Desc": "Accessory dwelling unit construction, attached to primary structure",
        },
        "adu",
    ),
    # 20. Other — County Fire / CF permit, no matching keywords
    (
        {
            "Type": "County Fire", "Sub_Type": "CF", "Category": "CF",
            "Work_Desc": "Fire sprinkler improvements for tenant space 2895 sq ft",
        },
        "other",
    ),
]


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_valid_output_categories():
    """Every result from classify_permit must be a member of CATEGORIES."""
    for row, _ in HAND_CLASSIFIED:
        result = classify_permit(row)
        assert result in CATEGORIES, (
            f"classify_permit returned {result!r} which is not in CATEGORIES"
        )


@pytest.mark.parametrize("row,expected", HAND_CLASSIFIED)
def test_hand_classified_sample(row, expected):
    assert classify_permit(row) == expected, (
        f"Expected {expected!r} for Sub_Type={row.get('Sub_Type')!r} "
        f"Work_Desc={row.get('Work_Desc', '')[:60]!r}"
    )
