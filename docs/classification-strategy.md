# Permit Classification Strategy

Categories returned by `classify_permit()` in `src/classifier.py`.

## Fields used

| Field | Role |
|---|---|
| `Sub_Type` | Primary signal — coded values are reliable across all four datasets |
| `Type` | Tiebreaker for residential vs commercial on new construction and remodel |
| `Category` | Secondary signal for electrical and mechanical (archive has richer values) |
| `Work_Desc` | Free-text fallback — used for ADU, solar, roofing, and MEP trades |

## Rule table (first match wins)

| Priority | Condition | Category |
|---|---|---|
| 1 | `Sub_Type` in {Demolition, Demolition Interior, Housing-Demo} | `demolition` |
| 2 | `Work_Desc` contains ADU keyword¹ | `adu` |
| 3 | `Sub_Type == "New Building"` and `Type == "Residential"` | `new_construction_residential` |
| 4 | `Sub_Type == "New Building"` and `Type != "Residential"` | `new_construction_commercial` |
| 5 | `Sub_Type` in {1-5, 5+, Production Permit} | `new_construction_residential` |
| 6 | `Sub_Type == "Addition"` | `addition` |
| 7 | `Work_Desc` contains solar keyword² | `solar` |
| 8 | `Work_Desc` contains roofing keyword³ | `roofing` |
| 9 | `Category` in electrical set⁴ OR `Work_Desc` contains electrical keyword⁵ | `electrical` |
| 10 | `Category == "HVAC"` OR `Work_Desc` contains mechanical keyword⁶ | `mechanical` |
| 11 | `Work_Desc` contains plumbing keyword⁷ | `plumbing` |
| 12 | `Sub_Type` in remodel set⁸ and `Type == "Residential"` | `remodel_residential` |
| 13 | `Sub_Type` in remodel set⁸ and `Type != "Residential"` | `remodel_commercial` |
| 14 | (fallback) | `other` |

## Keyword lists

¹ ADU: `adu`, `accessory dwelling`, `accessory unit`, `junior adu`, `jadu`

² Solar: `solar`, ` pv ` (space-padded), `pv system`, `photovoltaic`, `battery storage`

³ Roofing: `tear off`, `re-roof`, `reroof`, `shingle`, `squares of`, `roof`

⁴ Electrical categories: `Electric`, `Electrical`, `EV Charging Station`, `EV Station Electrical`

⁵ Electrical keywords: `electrical permit`, `panel change`, `panel upgrade`, `ev charger`, `electric vehicle`, `service upgrade`, `amp panel`, `amp service`

⁶ Mechanical keywords: `hvac`, `furnace`, `boiler`, `heat pump`, `split system`, `air handler`, `air condition`, `duct`

⁷ Plumbing keywords: `plumbing permit`, `plumb`, `water service`, `water heater`, `sewer`, `drain line`, `pipe replacement`

⁸ Remodel Sub_Types: `Remodel`, `Minor`, `Web-Minor`, `Housing-Minor`, `Housing-Rental Program-Minor`, `Housing-Rental Program`, `Housing Dept Permit`, `Phased`

## Design decisions

**ADU before new construction/addition (priority 2 before 3–6):** ADU permits
are filed under both New Building and Addition sub-types in Sacramento data.
Keyword detection on Work_Desc is more reliable than Sub_Type alone for ADUs.

**Solar before roofing (priority 7 before 8):** Work_Desc for rooftop solar
often contains the word "roof" (e.g. "roof-mount solar PV"). Solar must be
checked first so these are not misclassified as roofing.

**Electrical before mechanical (priority 9 before 10):** "Panel change-out"
permits are electrical; checking `electrical permit` and `panel change` before
mechanical keywords avoids any overlap.

**Generic `roof` keyword (priority 8):** Intentionally broad — covers "roof
replacement", "replace roof", etc. that lack "tear off" or "shingle". Solar is
checked first so "roof-mount solar" is never affected. The rare "roof drain"
plumbing permit would be misclassified here; in practice these are uncommon in
the SAC city dataset.

## Sub_Types intentionally mapped to `other`

`Pool`, `CF`, `Fire Equipment`, `Housing-Fire-Equipment`, `New Temp Power`,
`New Underground`, `New Foundation`, `New Grading`, `Moved Building`,
`Deferred Submittal`, `Master Plan`, `Sign` (Type=Sign), and any Sub_Type
not listed above.  Fire suppression (County Fire permits) also falls to `other`.
