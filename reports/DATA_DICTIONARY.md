# Data Dictionary

The dictionary describes the 25 source fields by their names and observed values. It does not independently verify the originating data collection definitions. The supplied file contains 240 rows.

| Column | Meaning in this project | Data type | Example / observed values |
|---|---|---|---|
| `accident_id` | Identifier for a recorded accident row | String | `IND-2022-0001`; unique in the supplied file |
| `date_time` | Recorded date and time associated with the accident | Date-time text, parsed to timestamp in processed data | `2022-01-10 05:15:00` |
| `year` | Recorded calendar year | Integer | 2021–2024 |
| `month` | Month label | Category/text | Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec |
| `state_ut` | Recorded State/UT label | Category/text | Karnataka, Telangana, Punjab |
| `district` | Recorded district label | Category/text | Mangaluru, Khammam, Patiala |
| `road_type` | Road category recorded for the accident | Category/text | National Highway, State Highway, City Road, Expressway, Rural Road |
| `weather` | Weather category recorded for the accident | Category/text | Clear, Dense Fog, Heavy Rain, Extreme Heat, Dust Storm |
| `road_surface` | Surface condition label | Category/text | Dry, Wet, Potholes / Unpaved, Loose Gravel |
| `lighting` | Lighting condition label | Category/text | Daylight, Dark / No Lights, Street Lights On |
| `vehicle_type` | Vehicle category recorded in the row | Category/text | Two-Wheeler, Truck / Heavy Goods, Car / SUV, Auto-Rickshaw, Bicycle / Pedestrian, Bus |
| `driver_age_group` | Driver age band label | Category/text | Underage (<18), 18-25, 26-40, 41-60, 60+ |
| `driver_gender` | Driver gender label | Category/text | Male, Female |
| `speed_limit_kmph` | Listed speed limit, in kilometres per hour | Numeric (integer in supplied file) | 50–120 |
| `estimated_speed_kmph` | Estimated speed, in kilometres per hour | Numeric (integer in supplied file) | 40–175 |
| `alcohol_involved` | Whether the row is marked as alcohol-involved | Boolean | TRUE, FALSE |
| `helmet_seatbelt_used` | Combined helmet/seatbelt usage flag as supplied | Boolean | TRUE, FALSE; applicability may vary by vehicle |
| `severity` | Recorded severity label | Category/text | Fatal, Grievous Injury, Minor Injury, Property Damage Only |
| `fatalities` | Fatality count recorded for the accident row | Non-negative integer count | 0–2 in the supplied file |
| `severe_injuries` | Severe injury count recorded for the row | Non-negative integer count | 0–3 in the supplied file |
| `minor_injuries` | Minor injury count recorded for the row | Non-negative integer count | 0–3 in the supplied file |
| `primary_cause` | Primary cause label supplied in the record | Category/text | Overspeeding, Drunk Driving, Weather Visibility, Wrong-Side Driving, Fatigue / Sleep, Mobile Phone Use, Red Light / Signal Jump, Pothole / Road Defect |
| `pedestrians_involved` | Whether the row is marked as involving pedestrians | Boolean | TRUE, FALSE |
| `latitude` | Latitude coordinate supplied with the record | Decimal number | 8.2757–31.7208 in this file |
| `longitude` | Longitude coordinate supplied with the record | Decimal number | 68.0551–91.9811 in this file |

## Derived fields and aggregate measures

`data/processed/extracted_accidents.csv` is a compact table keyed by `accident_id`; it derives `accident_date` and `accident_hour` from `date_time`, and `month_number` from its calendar month. `nonfatal_injuries` is the sum of severe and minor injuries (fatalities are separate). Aggregate tables contain `accident_count`, outcome totals, and Boolean-flagged record counts. `above_speed_limit_records` counts rows where `estimated_speed_kmph` is greater than `speed_limit_kmph`. These derived metrics are arithmetic summaries, not additional observations.
