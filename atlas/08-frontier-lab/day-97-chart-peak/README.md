# A Chart with an Expected Peak

**Day 97** · **Advanced** · Phase 08: Frontier Lab

Read a chart you render to SVG, answer the peak with a tolerance, and refuse a chart whose axis is cut.

## Concept

People paste charts into chats and ask for the peak. The model answers with a number that is hard to audit. This project renders a tiny bar chart to SVG from a data table, then answers "what is the peak" by reading the SVG's data attributes, not by eyeballing pixels. The expected answer is the max value in the table, and the tolerance is zero because you control the source. A second chart cuts the axis so the bars start at a non-zero baseline. The required behavior is to refuse with reason `cut-axis`, because a visual comparison would mislead, even though the data attribute still holds the true value. You will test both. The point is an answer policy for a figure, not a vision-model benchmark.

## Approach

The SVG writer puts `data-value` and `data-baseline` on each bar. The reader refuses if any baseline is not zero. Otherwise it returns the max `data-value` and the category. A test tampers with a `data-value` so it no longer matches the source table and expects the reader to fail a consistency check you also run: every data value must appear in the source table. That check stops a chart that was edited by hand from being treated as authoritative over the table. The table remains the source of truth. The SVG is a view.

## Components

| Piece | Role |
| --- | --- |
| Table source | Categories and values. |
| SVG writer | Bars with data attributes and a baseline. |
| Reader | Returns the peak or a refusal. |
| Consistency check | Data attributes must match the table. |

## How it works

1. Render a normal chart and read the peak.
2. Assert the category and the value match the table max.
3. Render a cut-axis chart and expect `cut-axis`.
4. Tamper a data attribute and expect a consistency failure.
5. Document that the table, not the picture, is authoritative.

## Tech stack

- Python 3.11 or newer
- SVG as text
- No vision model and no browser

## Setup

1. Create `chart-peak/` with `chart.py`, `read.py`, and tests.
2. Write both SVGs to `out/`.
3. Run tests.
4. Open the SVG in a browser if you want to see it, but the tests must not require that.

## What done looks like

- The zero-baseline chart returns the true peak category and value.
- The cut-axis chart is refused.
- A tampered attribute fails the consistency check.
- The notes name the table as the source of truth.

## Step ahead

A second question asks for the trough, and a missing category should not be treated as zero. Add a trough reader that ignores categories listed in `not_observed` rather than treating them as value zero. Fixture a week with a missing day and show the trough computed on observed days only, plus a refusal if fewer than three days were observed. The follow-on is an answer that knows the difference between a measured zero and a gap.
