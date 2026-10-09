# cfb-viz

**A Python visualization library for college football.**

> **Current development version: v0.1.0 (pre-release)**  
> **Status:** Early development — designing the schedule matrix data contract.

## Overview

`cfb-viz` aims to make it easier to create clean, customizable, publication-quality college football visualizations using Python and Matplotlib.

Instead of repeatedly writing custom plotting code, users will eventually be able to generate common college football visualizations through simple, reusable functions.

The project initially focuses on NCAA Division I FBS football.

## Development Status

### Current Progress

- [x] Initialize Python package using `uv`
- [x] Set up Git and GitHub repository
- [x] Define the schedule DataFrame structure
- [x] Implement schedule data validation
- [x] Write automated validation tests using `pytest`
- [ ] Address additional validation edge cases
- [ ] Implement schedule matrix visualization
- [ ] Add visualization customization options

## Schedule Data Format

The schedule validator expects a pandas DataFrame containing one row per game.

| Column | Type | Description |
|---|---|---|
| `week` | Integer | Positive week number |
| `home_team` | String | Officially designated home team |
| `away_team` | String | Officially designated away team |
| `neutral_site` | Boolean | Whether the game is played at a neutral site |

Additional columns are permitted.

**Note:** Week 0 support is planned but has not yet been implemented.

## Schedule Validation

The `validate_schedule()` function, located in `cfb_viz.validation`, checks:

- Input is a pandas DataFrame
- Required columns are present
- Week numbers are valid
- Team names are nonempty strings
- Teams do not play against themselves
- Neutral-site values are boolean
- Duplicate games are rejected
- Teams do not play multiple games in the same week

Invalid schedules raise a `TypeError` or `ValueError` with a descriptive message.

## Testing

Automated tests are written using `pytest` and located in `tests/test_validation.py`.

Run the test suite:

```bash
uv run pytest -v
```

The current validation test suite passes. Additional edge-case testing is planned before the visualization API is implemented.


## Technology

- Python
- pandas
- NumPy
- Matplotlib
- pytest
- uv

## Project Philosophy

- `cfb-viz` is primarily a **visualization library**, not a data collection or statistical analysis package.
- The initial release will focus on accepting user-provided data and turning it into reusable visualizations.
- Automatic data retrieval and advanced analytics are outside the scope of v0.1.0.

## Contribution

This project is under active development. Its public API and data requirements are not yet finalized.
feedbacks and suggestions will be welcome as the project develops, but we are not accepting any pull request at this moment.