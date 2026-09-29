# Results Summary

## Dataset and method

This report is computed from `india_road_accidents_dataset.csv`, the user-provided accident-level CSV. The loaded source had 240 rows and 25 columns. 240 records were included in this run; 240 remain after exact duplicate-row handling. This dataset is not asserted to be a complete official or nationally representative record of Indian road accidents.

## Key findings observed in these records

- Maharashtra has the most recorded accidents by State/UT (24 records in this dataset).
- Maharashtra has the highest recorded fatalities by State/UT (18 records in this dataset).
- Fatal has the most frequent recorded severity (118 records in this dataset).
- Overspeeding has the most frequently recorded primary cause (74 records in this dataset).
- Two-Wheeler has the most frequently recorded vehicle type (81 records in this dataset).
- Clear has the highest recorded weather category count (85 records in this dataset).
- Daylight has the highest recorded lighting category count (135 records in this dataset).
- National Highway has the highest recorded road type count (75 records in this dataset).
- 26-40 has the most frequent recorded driver age group (69 records in this dataset).
- Accident records by year: 2021: 62; 2022: 57; 2023: 49; 2024: 72
- Sep has the highest recorded month count (31).
- 52 of 240 records (21.7%) are marked alcohol-involved.
- 71 of 240 records (29.6%) are marked pedestrian-involved.
- Estimated speed exceeds the listed speed limit in 196 of 240 records with both values (81.7%); mean estimated-minus-limit difference is 18.7 km/h.
- Drunk Driving has the highest recorded fatality total by primary cause (58 fatalities); this is an observed association, not evidence of causation.

## Accidents by year

| year | accident_count |
| --- | --- |
| 2021 | 62 |
| 2022 | 57 |
| 2023 | 49 |
| 2024 | 72 |
## Accidents by State/UT

| state_ut | accident_count |
| --- | --- |
| Maharashtra | 24 |
| Assam | 19 |
| Telangana | 19 |
| Delhi NCR | 17 |
| Uttar Pradesh | 17 |
| Andhra Pradesh | 16 |
| Gujarat | 16 |
| Rajasthan | 15 |
| Punjab | 14 |
| West Bengal | 14 |
| Bihar | 12 |
| Kerala | 12 |
| Madhya Pradesh | 12 |
| Tamil Nadu | 12 |
| Odisha | 11 |
## Fatalities by State/UT

| state_ut | fatalities |
| --- | --- |
| Maharashtra | 18.0 |
| Assam | 15.0 |
| Telangana | 13.0 |
| Delhi NCR | 12.0 |
| Gujarat | 12.0 |
| Rajasthan | 12.0 |
| Punjab | 11.0 |
| Tamil Nadu | 11.0 |
| Madhya Pradesh | 10.0 |
| Uttar Pradesh | 10.0 |
| West Bengal | 10.0 |
| Kerala | 9.0 |
| Andhra Pradesh | 9.0 |
| Karnataka | 7.0 |
| Bihar | 6.0 |
## Severity distribution

| severity | accident_count |
| --- | --- |
| Fatal | 118 |
| Grievous Injury | 75 |
| Minor Injury | 42 |
| Property Damage Only | 5 |
## Primary cause and recorded fatal outcomes

| primary_cause | accident_count | fatal_accident_count | fatalities |
| --- | --- | --- | --- |
| Drunk Driving | 46 | 40 | 58.0 |
| Overspeeding | 74 | 37 | 54.0 |
| Mobile Phone Use | 17 | 9 | 13.0 |
| Wrong-Side Driving | 28 | 9 | 12.0 |
| Red Light / Signal Jump | 17 | 6 | 10.0 |
| Weather Visibility | 29 | 8 | 9.0 |
| Pothole / Road Defect | 11 | 5 | 8.0 |
| Fatigue / Sleep | 18 | 4 | 7.0 |

## Data quality

```json
{
  "before": {
    "rows": 240,
    "columns": 25,
    "missing_cells": 0,
    "missing_by_column": {
      "accident_id": 0,
      "date_time": 0,
      "year": 0,
      "month": 0,
      "state_ut": 0,
      "district": 0,
      "road_type": 0,
      "weather": 0,
      "road_surface": 0,
      "lighting": 0,
      "vehicle_type": 0,
      "driver_age_group": 0,
      "driver_gender": 0,
      "speed_limit_kmph": 0,
      "estimated_speed_kmph": 0,
      "alcohol_involved": 0,
      "helmet_seatbelt_used": 0,
      "severity": 0,
      "fatalities": 0,
      "severe_injuries": 0,
      "minor_injuries": 0,
      "primary_cause": 0,
      "pedestrians_involved": 0,
      "latitude": 0,
      "longitude": 0
    },
    "duplicate_rows": 0,
    "duplicate_accident_ids": 0,
    "invalid_values": {
      "date_time": 0,
      "year": 0,
      "year_date_mismatch": 0,
      "month": 0,
      "month_date_mismatch": 0,
      "speed_limit_kmph": 0,
      "estimated_speed_kmph": 0,
      "fatalities": 0,
      "severe_injuries": 0,
      "minor_injuries": 0,
      "latitude": 0,
      "longitude": 0,
      "severity": 0,
      "driver_gender": 0,
      "alcohol_involved": 0,
      "helmet_seatbelt_used": 0,
      "pedestrians_involved": 0
    }
  },
  "after": {
    "rows": 240,
    "columns": 25,
    "missing_cells": 0,
    "missing_by_column": {
      "accident_id": 0,
      "date_time": 0,
      "year": 0,
      "month": 0,
      "state_ut": 0,
      "district": 0,
      "road_type": 0,
      "weather": 0,
      "road_surface": 0,
      "lighting": 0,
      "vehicle_type": 0,
      "driver_age_group": 0,
      "driver_gender": 0,
      "speed_limit_kmph": 0,
      "estimated_speed_kmph": 0,
      "alcohol_involved": 0,
      "helmet_seatbelt_used": 0,
      "severity": 0,
      "fatalities": 0,
      "severe_injuries": 0,
      "minor_injuries": 0,
      "primary_cause": 0,
      "pedestrians_involved": 0,
      "latitude": 0,
      "longitude": 0
    },
    "duplicate_rows": 0,
    "duplicate_accident_ids": 0,
    "invalid_values": {
      "date_time": 0,
      "year": 0,
      "year_date_mismatch": 0,
      "month": 0,
      "month_date_mismatch": 0,
      "speed_limit_kmph": 0,
      "estimated_speed_kmph": 0,
      "fatalities": 0,
      "severe_injuries": 0,
      "minor_injuries": 0,
      "latitude": 0,
      "longitude": 0,
      "severity": 0,
      "driver_gender": 0,
      "alcohol_involved": 0,
      "helmet_seatbelt_used": 0,
      "pedestrians_involved": 0
    },
    "exact_duplicate_rows_removed": 0
  },
  "handling": "Invalid typed/domain values become missing in the processed copy and are counted; no values are imputed. Exact duplicate rows are removed from the processed copy. Duplicate IDs are reported, not silently discarded. The raw source is never changed."
}
```

## Interpretation and limitations

Results describe counts and values recorded in this supplied dataset only. They do not establish that a road, weather condition, driver group, or behavior caused an accident. The source's collection method, sampling coverage, and representativeness are not established by the CSV alone. `helmet_seatbelt_used` combines two safety-device concepts in one field, so applicability can differ by vehicle. Coordinates are summarized as supplied and are not independently verified.

## Reproducibility

From the project root, run `python -m src.run_pipeline` or `python run_pipeline.py`. The raw source is read only; processed files, aggregate tables, figures, and this report are regenerated from it.
