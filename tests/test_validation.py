import pandas as pd
from cfb_viz.validation import validate_schedule
import pytest  # type: ignore


@pytest.mark.parametrize("value", [None, 123, "schedule", [], {}])
def test_invalid_dataframe(value):
    with pytest.raises(TypeError, match="Expected a pandas DataFrame"):
        validate_schedule(value)


def test_valid_schedule():
    df = pd.DataFrame(
        {
            "week": [1, 2],
            "home_team": ["Alabama", "Georgia"],
            "away_team": ["LSU", "Tennessee"],
            "neutral_site": [False, False],
        }
    )

    validate_schedule(df)


def test_negative_week():
    df = pd.DataFrame(
        {
            "week": [1, -2],
            "home_team": ["Alabama", "Georgia"],
            "away_team": ["LSU", "Tennessee"],
            "neutral_site": [False, False],
        }
    )

    with pytest.raises(ValueError, match="week must contain nonnegative integers"):
        validate_schedule(df)


def test_missing_columns():
    df = pd.DataFrame(
        {
            "week": [1, 2],
            "home_team": ["Alabama", "Georgia"],
            "away_team": ["LSU", "Tennessee"],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_schedule(df)


@pytest.mark.parametrize("week", [-1, 2.5, "3"])
def test_invalid_week(week):
    df = pd.DataFrame(
        {
            "week": [week],
            "home_team": ["Alabama"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    with pytest.raises(ValueError, match="week must contain nonnegative integers"):
        validate_schedule(df)


def test_week_zero():
    df = pd.DataFrame(
        {
            "week": [0],
            "home_team": ["Alabama"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    validate_schedule(df)


@pytest.mark.parametrize("column", ["home_team", "away_team"])
@pytest.mark.parametrize("name", ["", "   ", None, 123])
def test_invalid_team(column, name):
    df = pd.DataFrame(
        {
            "week": [1],
            "home_team": ["Alabama"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    df[column] = df[column].astype(object)
    df.loc[0, column] = name

    with pytest.raises(ValueError, match="team name must contain nonempty strings"):
        validate_schedule(df)


@pytest.mark.parametrize("value", [0, 1, "True", None, 2.5])
def test_invalid_neutral_site(value):
    df = pd.DataFrame(
        {
            "week": [1],
            "home_team": ["Alabama"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    df["neutral_site"] = df["neutral_site"].astype(object)
    df.loc[0, "neutral_site"] = value

    with pytest.raises(ValueError, match="neutral_site must contain boolean values"):
        validate_schedule(df)


def test_team_playing_itself():
    df = pd.DataFrame(
        {
            "week": [1],
            "home_team": ["Alabama"],
            "away_team": ["Alabama"],
            "neutral_site": [False],
        }
    )

    with pytest.raises(ValueError, match="A team cannot play against itself"):
        validate_schedule(df)


def test_duplicate_games():
    df = pd.DataFrame(
        {
            "week": [1, 2, 1],
            "home_team": ["Alabama", "Georgia", "Alabama"],
            "away_team": ["LSU", "Tennessee", "LSU"],
            "neutral_site": [False, False, False],
        }
    )

    with pytest.raises(ValueError, match="Duplicate games detected"):
        validate_schedule(df)


def test_multiple_games_same_week():
    df = pd.DataFrame(
        {
            "week": [1, 1, 2],
            "home_team": ["Alabama", "Georgia", "Tennessee"],
            "away_team": ["LSU", "Alabama", "Florida"],
            "neutral_site": [False, False, False],
        }
    )

    with pytest.raises(
        ValueError, match="A team cannot play multiple games in the same week"
    ):
        validate_schedule(df)


@pytest.mark.parametrize("name", [" Alabama", "Alabama ", " Alabama "])
def test_team_name_whitespace(name):
    df = pd.DataFrame(
        {
            "week": [1],
            "home_team": ["Georgia"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    df.loc[0, "home_team"] = name

    with pytest.raises(
        ValueError, match="team names must not contain leading or trailing whitespace"
    ):
        validate_schedule(df)


def test_empty_schedule():
    df = pd.DataFrame(columns=["week", "home_team", "away_team", "neutral_site"])

    with pytest.raises(ValueError, match="Schedule cannot be empty"):
        validate_schedule(df)


def test_extra_columns():
    df = pd.DataFrame(
        {
            "week": [1],
            "home_team": ["Georgia"],
            "away_team": ["LSU"],
            "neutral_site": [False],
            "home_score": [28],
            "away_score": [21],
        }
    )

    validate_schedule(df)
