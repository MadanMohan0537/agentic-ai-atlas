# Seasonal Residuals

**Day 88** · **Advanced** · Phase 07: Flowroom: Analytics and Pipelines

Alert when a daily rental count departs from a weekday baseline, and suppress dates you listed in advance.

## Concept

A raw spike on Saturday is not news if Saturdays are always busy. This project builds a baseline for daily completed rentals: the median of the same weekday over the previous eight weeks, computed only from dates before the day you are scoring. The residual is the day's count minus that median. An alert fires when the residual exceeds a threshold you set in advance. You will plant one holiday that looks like an alert and, in the step that is still the core project, let it alert. The suppression list comes in the follow-on. For the core, you will also plant a true quiet Tuesday that should alert, and a normal Saturday that should not. This is a residual check on a metric series. It is not a feature-drift monitor and it does not recommend retraining a model.

## Approach

The series is a CSV of date and count that you generate with a weekday pattern plus two anomalies. The baseline function refuses to use the current day or any later day. A test passes future dates into the frame and asserts the baseline for a Wednesday does not change when a later Wednesday is huge. The threshold is a constant in `threshold.txt`. Alerts are rows in `alerts.csv` with the date, the median, the count, and the residual. No alert row means no alert. Do not emit a score for every day and call them all alerts.

## Components

| Piece | Role |
| --- | --- |
| Weekday median | Eight prior matching weekdays, looking only backward. |
| Residual | Count minus median. |
| Threshold file | Written before you interpret alerts. |
| Alert file | Only the days that crossed the threshold. |

## How it works

1. Generate eight weeks of patterned counts plus a quiet Tuesday and a busy holiday Monday.
2. Compute baselines and assert a future leak does not change an earlier baseline.
3. Write alerts using the threshold.
4. Assert the normal Saturday is absent and the quiet Tuesday is present.
5. Leave the holiday in the alert file for the core project and mention it in the notes as the known nuisance.

## Tech stack

- Python 3.11 or newer
- Standard library `statistics` and `datetime`
- CSV inputs and outputs

## Setup

1. Create `residuals/` with `series.csv`, `baseline.py`, and tests.
2. Set the threshold before running alerts.
3. Run the job and the leak test.
4. Run tests.

## What done looks like

- The baseline for a day does not depend on later days.
- The quiet Tuesday alerts and a normal Saturday does not.
- The holiday Monday is listed as a nuisance in the notes, and it does alert in the core output.
- Non-alerting days are absent from `alerts.csv`.

## Step ahead

Add `calendar.csv` of dates that should not alert, written before you rerun, and suppress those dates with a reason `calendar` stored in a separate file from the real alerts. The quiet Tuesday must remain a real alert. A date on the calendar that would not have alerted anyway should not appear as a suppression, so you do not inflate how useful the calendar is. The follow-on is a suppression log you can audit, not a deleted residual.
