# Sacramento Building Permit Schemas
Scraped: 2026-05-27  |  Source: Sacramento ArcGIS Hub

---

## Issued Building Permits — Current Year
**Item ID**: `671459cd783247bc9108132252bf3453`  
**Service URL**: https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/BldgPermitIssued_CurrentYear/FeatureServer/0  
**Total records**: 6,089  

### Fields
| Field | Type | Alias | Populated in sample |
|---|---|---|---|
| `OBJECTID` | OID | OBJECTID | yes |
| `Type` | String | Type | yes |
| `Sub_Type` | String | Sub_Type | yes |
| `Category` | String | Category | yes |
| `Application` | String | Application | yes |
| `Rpt_Status` | String | Rpt_Status | yes |
| `Status_Date` | String | Status_Date | yes |
| `Current_Status` | String | Current_Status | yes |
| `Parcel_No` | String | Parcel_No | yes |
| `Address` | String | Address | yes |
| `Site_Location` | String | Site_Location | yes (1/10) |
| `ZIP` | String | ZIP | yes |
| `Inspection_District` | String | Inspection_District | yes (9/10) |
| `House_Count` | Integer | House_Count | yes (6/10) |
| `Project_Sq_Ft` | Double | Project_Sq_Ft | yes (2/10) |
| `Habitable_Sq_Ft` | Double | Habitable_Sq_Ft | yes (1/10) |
| `Valuation` | Double | Valuation | yes |
| `Activity_Code` | String | Activity_Code | yes (3/10) |
| `Contractor` | String | Contractor | yes (9/10) |
| `Council_Dist` | String | Council_Dist | yes (3/10) |
| `Comm_Plan_Area` | String | Comm_Plan_Area | yes (3/10) |
| `Work_Desc` | String | Work_Desc | yes |
| `Project_Name` | String | Project_Name | yes (7/10) |

### Key field notes
- **Parcel_No** (String) — yes  — e.g. `"03601330010000"`
- **Type** (String) — yes
  - Distinct values: Commercial, County Fire, Facilities Permit Program, Residential, Sign
- **Sub_Type** (String) — yes
  - Distinct values: 1-5, 5+, Addition, CF, Demolition, Demolition Interior, Fire Equipment, Housing Dept Permit, Housing-Demo, Housing-Minor, Housing-Rental Program-Minor, Minor, New Building, New Temp Power, New Underground, Other Struct (non-bldg), Phased, Pool, Production Permit, Remodel … (23 total)
- **Category** (String) — yes
  - Distinct values: Amusement, Apts 3-4, Apts 5+, CF, Churches, Condos, Duplex, EV Charging Station, Half Plex, Hospitals, Hotel or Motel, Industrial, Manuf Bldg, Mix-Use, NA, Office, Other Non-Res Bldgs, Other Struct (non-bldg), Private Garage, Public Parking … (26 total)
- **Valuation** (Double) — yes  — e.g. `"17438"`
- **Work_Desc** (String) — yes  — e.g. `"E-Permit: Tear Off - Yes, Resheet - No, 2 layer(s), 23 squares of Composite Class A. In-progress ins"`
- **Application** (String) — yes  — e.g. `"RES-2600002"`

---

## Issued Building Permits — Archive
**Item ID**: `ec9060482ef749899bb20f6dc8003530`  
**Service URL**: https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/BldgPermitIssued_Archive/FeatureServer/0  
**Total records**: 200,913  

### Fields
| Field | Type | Alias | Populated in sample |
|---|---|---|---|
| `OBJECTID` | OID | OBJECTID | yes |
| `Type` | String | Type | yes |
| `Sub_Type` | String | Sub_Type | yes |
| `Category` | String | Category | yes |
| `Application` | String | Application | yes |
| `Rpt_Status` | String | Rpt_Status | yes |
| `Status_Date` | String | Status_Date | yes |
| `Current_Status` | String | Current_Status | yes |
| `Parcel_No` | String | Parcel_No | yes |
| `Address` | String | Address | yes |
| `Site_Location` | String | Site_Location | no |
| `ZIP` | String | ZIP | yes |
| `Inspection_District` | String | Inspection_District | yes |
| `House_Count` | Integer | House_Count | yes (5/10) |
| `Project_Sq_Ft` | Double | Project_Sq_Ft | no |
| `Habitable_Sq_Ft` | Double | Habitable_Sq_Ft | no |
| `Valuation` | Double | Valuation | yes |
| `Activity_Code` | String | Activity_Code | no |
| `Contractor` | String | Contractor | yes |
| `Council_Dist` | String | Council_Dist | no |
| `Comm_Plan_Area` | String | Comm_Plan_Area | no |
| `Work_Desc` | String | Work_Desc | yes |
| `Project_Name` | String | Project_Name | yes (5/10) |

### Key field notes
- **Parcel_No** (String) — yes  — e.g. `"01401610300000"`
- **Type** (String) — yes
  - Distinct values: Commercial, County Fire, Facilities Permit Program, Residential, Sign
- **Sub_Type** (String) — yes
  - Distinct values: 1-5, 5+, Addition, CF, Demolition, Demolition Interior, Fire Equipment, Fire-Equipment, Housing Dept Permit, Housing-Demo, Housing-Fire-Equipment, Housing-Minor, Housing-Rental Program, Housing-Rental Program-Minor, Minor, Moved Building, New Building, New Foundation, New Grading, New Structural … (30 total)
- **Category** (String) — yes
  - Distinct values: APT, Above Ground Pool, Above ground spa, Amusement, Apts 3-4, Apts 5+, CF, Churches, Commercial, Commercial Pool, Condos, Duplex, EV Charging Station, Electric, Electrical, HVAC, Half Plex, Half-Plex, Hospitals, Hotel or Motel … (87 total)
- **Valuation** (Double) — yes  — e.g. `"0"`
- **Work_Desc** (String) — yes  — e.g. `"E-Permit: Water Service replacement or repair, 60 L.F. Drain Line replacement or repair, 25 L.F. Wat"`
- **Application** (String) — yes  — e.g. `"RES-1600001"`

---

## Applied Building Permits — Current Year
**Item ID**: `8d18bce2cecb4392b28d42015002c77f`  
**Service URL**: https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/BldgPermitApplied_CurrentYear/FeatureServer/0  
**Total records**: 6,675  

### Fields
| Field | Type | Alias | Populated in sample |
|---|---|---|---|
| `OBJECTID` | OID | OBJECTID | yes |
| `Type` | String | Type | yes |
| `Sub_Type` | String | Sub_Type | yes |
| `Category` | String | Category | yes |
| `Application` | String | Application | yes |
| `Rpt_Status` | String | Rpt_Status | yes |
| `Status_Date` | String | Status_Date | yes |
| `Current_Status` | String | Current_Status | yes |
| `Parcel_No` | String | Parcel_No | yes |
| `Address` | String | Address | yes |
| `Site_Location` | String | Site_Location | no |
| `ZIP` | String | ZIP | yes |
| `Inspection_District` | String | Inspection_District | yes (9/10) |
| `House_Count` | Integer | House_Count | yes (6/10) |
| `Project_Sq_Ft` | Double | Project_Sq_Ft | yes (2/10) |
| `Habitable_Sq_Ft` | Double | Habitable_Sq_Ft | no |
| `Valuation` | Double | Valuation | yes |
| `Activity_Code` | String | Activity_Code | yes (3/10) |
| `Contractor` | String | Contractor | yes (9/10) |
| `Council_Dist` | String | Council_Dist | yes (4/10) |
| `Comm_Plan_Area` | String | Comm_Plan_Area | yes (4/10) |
| `Work_Desc` | String | Work_Desc | yes |
| `Project_Name` | String | Project_Name | yes (7/10) |

### Key field notes
- **Parcel_No** (String) — yes  — e.g. `"03601330010000"`
- **Type** (String) — yes
  - Distinct values: Commercial, County Fire, Facilities Permit Program, Residential, Sign
- **Sub_Type** (String) — yes
  - Distinct values: 1-5, 5+, Addition, CF, Deferred Submittal, Demolition, Demolition Interior, Fire Equipment, Housing Dept Permit, Housing-Demo, Housing-Minor, Housing-Rental Program-Minor, Master Plan, Minor, New Building, New Structural, New Temp Power, Other Struct (non-bldg), Phased, Pool … (26 total)
- **Category** (String) — yes
  - Distinct values: Amusement, Apts 3-4, Apts 5+, CF, Churches, Condos, Demolition, Duplex, EV Charging Station, EV Station Electrical, Electrical, Fire, Fire-Alarm System, Fire-Fire Sprinklers, Half Plex, Hospitals, Hotel or Motel, Industrial, Mix-Use, NA … (37 total)
- **Valuation** (Double) — yes  — e.g. `"17438"`
- **Work_Desc** (String) — yes  — e.g. `"E-Permit: Tear Off - Yes, Resheet - No, 2 layer(s), 23 squares of Composite Class A. In-progress ins"`
- **Application** (String) — yes  — e.g. `"RES-2600002"`

---

## Applied Building Permits — Archive
**Item ID**: `3b579cafcecc406b8680c56dbd4e7bbb`  
**Service URL**: https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/BldgPermitApplied_Archive/FeatureServer/0  
**Total records**: 228,126  

### Fields
| Field | Type | Alias | Populated in sample |
|---|---|---|---|
| `OBJECTID` | OID | OBJECTID | yes |
| `Type` | String | Type | yes |
| `Sub_Type` | String | Sub_Type | yes |
| `Category` | String | Category | yes |
| `Application` | String | Application | yes |
| `Rpt_Status` | String | Rpt_Status | yes |
| `Status_Date` | String | Status_Date | yes |
| `Current_Status` | String | Current_Status | yes |
| `Parcel_No` | String | Parcel_No | yes |
| `Address` | String | Address | yes |
| `Site_Location` | String | Site_Location | yes (1/10) |
| `ZIP` | String | ZIP | yes |
| `Inspection_District` | String | Inspection_District | yes (9/10) |
| `House_Count` | Integer | House_Count | yes (5/10) |
| `Project_Sq_Ft` | Double | Project_Sq_Ft | yes (4/10) |
| `Habitable_Sq_Ft` | Double | Habitable_Sq_Ft | yes (2/10) |
| `Valuation` | Double | Valuation | yes |
| `Activity_Code` | String | Activity_Code | yes (1/10) |
| `Contractor` | String | Contractor | yes (8/10) |
| `Council_Dist` | String | Council_Dist | yes (4/10) |
| `Comm_Plan_Area` | String | Comm_Plan_Area | yes (4/10) |
| `Work_Desc` | String | Work_Desc | yes |
| `Project_Name` | String | Project_Name | yes (5/10) |

### Key field notes
- **Parcel_No** (String) — yes  — e.g. `"01401610300000"`
- **Type** (String) — yes
  - Distinct values: Commercial, County Fire, Facilities Permit Program, Residential, Sign
- **Sub_Type** (String) — yes
  - Distinct values: 1-5, 5+, Addition, CF, Deferred Submittal, Demolition, Demolition Interior, Fire Equipment, Fire-Equipment, Housing Dept Permit, Housing-Demo, Housing-Fire-Equipment, Housing-Minor, Housing-Rental Program, Housing-Rental Program-Minor, Master Plan, Minor, Moved Building, New Building, New Foundation … (34 total)
- **Category** (String) — yes
  - Distinct values: 191NA, APT, Above Ground Pool, Above ground spa, Amusement, Apt 5+, Apts 3-4, Apts 5+, Bar, CELL TOWER, CF, Churches, Commercial, Commercial Pool, Condos, Demolition, Detached Garage, Dumbwaiter Specifications, Duplex, EV Charging Station … (133 total)
- **Valuation** (Double) — yes  — e.g. `"0"`
- **Work_Desc** (String) — yes  — e.g. `"E-Permit: Water Service replacement or repair, 60 L.F. Drain Line replacement or repair, 25 L.F. Wat"`
- **Application** (String) — yes  — e.g. `"RES-1600001"`
