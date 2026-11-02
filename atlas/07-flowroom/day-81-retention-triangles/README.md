# Retention Triangles

**Day 81** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Build a cohort retention triangle from signup week and activity week, and do not fill future weeks.

## Concept

A retention chart that shows every cohort at week 4, including the cohort that signed up last week, is fiction. This project builds a triangle. Rows are signup cohorts by week. Columns are week 0 through week 4. A cell is the fraction of the cohort with at least one rental in that activity week. Cells in the future, relative to a `as_of` date you set, are null, not zero. Zero would say the riders churned. Null says the week has not happened. You will compute the triangle from a fixture that includes a cohort with a full history and a cohort that started near `as_of`. The report prints nulls as blank. A test expects a blank, and it fails if you write 0.

## Approach

Signup week is the week of the rider's first event in a signup file, not the first event you happened to load if the file is filtered. Use the signup file as the source of the cohort so a late first rental does not move the rider. Activity is a set of weeks per rider. Cohort size is the number of riders in the signup week, including those with no later rentals. They count in the denominator. Week 0 includes the signup week itself. Document that. Pick ISO weeks and a single time zone, and parse every timestamp as aware UTC converted to that zone before you take the week.

## Components

| Piece | Role |
| --- | --- |
| Signup file | Rider id and signup timestamp, the cohort source. |
| Activity file | Rentals after signup. |
| Triangle | Cohort by relative week, with nulls for the future. |
| As-of date | The clock the null rule uses. |

## How it works

1. Build cohorts from the signup file.
2. Mark activity weeks per rider.
3. Fill cells up to the last completed week relative to `as_of`.
4. Leave future cells null and test one of them.
5. Include a rider with no activity and assert they remain in the denominator.

## Tech stack

- Python 3.11 or newer
- Standard library `datetime` and `csv`
- A printed triangle in markdown or CSV

## Setup

1. Create `retention/` with the two CSV files, `triangle.py`, and tests.
2. Run the triangle at a fixed `as_of` you store in `as_of.txt`.
3. Run tests.
4. Read the triangle and confirm the newest cohort has blanks on the right.

## What done looks like

- Future cells are null, and a test rejects zeros in those cells.
- Inactive signups stay in the denominator.
- The as-of date is a file, not today's date from the clock.
- Week boundaries use one named time zone.
