import pandas as pd
import pytest  # type: ignore
from pandas.testing import assert_frame_equal

from cfb_viz.schedule import prepare_schedule


def test_home_away():
    df = pd.DataFrame(
        {
            "week": [1],
            "home_team": ["Alabama"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    matrix = prepare_schedule(df)

    assert matrix.loc["Alabama", 1] == "H"
    assert matrix.loc["LSU", 1] == "A"


def test_neutral_site():
    df = pd.DataFrame(
        {
            "week": [2],
            "home_team": ["Georgia"],
            "away_team": ["Tennessee"],
            "neutral_site": [True],
        }
    )

    matrix = prepare_schedule(df)

    assert matrix.loc["Georgia", 2] == "N"
    assert matrix.loc["Tennessee", 2] == "N"


def test_bye_week():
    df = pd.DataFrame(
        {
            "week": [1, 2],
            "home_team": ["Alabama", "Georgia"],
            "away_team": ["LSU", "Tennessee"],
            "neutral_site": [False, False],
        }
    )

    matrix = prepare_schedule(df)

    assert matrix.loc["Alabama", 2] == "BYE"
    assert matrix.loc["LSU", 2] == "BYE"
    assert matrix.loc["Georgia", 1] == "BYE"
    assert matrix.loc["Tennessee", 1] == "BYE"


def test_missing_week():
    df = pd.DataFrame(
        {
            "week": [1, 3],
            "home_team": ["Alabama", "Georgia"],
            "away_team": ["LSU", "Tennessee"],
            "neutral_site": [False, False],
        }
    )

    matrix = prepare_schedule(df)

    assert list(matrix.columns) == [1, 2, 3]
    assert (matrix[2] == "BYE").all()


def test_multiple_games():
    df = pd.DataFrame(
        {
            "week": [1, 1, 2, 2],
            "home_team": ["Alabama", "Georgia", "LSU", "Tennessee"],
            "away_team": ["LSU", "Tennessee", "Georgia", "Alabama"],
            "neutral_site": [False, True, False, False],
        }
    )

    matrix = prepare_schedule(df)

    expected = pd.DataFrame(
        {
            1: ["H", "N", "A", "N"],
            2: ["A", "A", "H", "H"],
        },
        index=pd.Index(
            ["Alabama", "Georgia", "LSU", "Tennessee"],
            name="team",
        ),
    )
    expected.columns.name = "week"

    assert_frame_equal(matrix, expected)


def test_week_zero():
    df = pd.DataFrame(
        {
            "week": [0, 2],
            "home_team": ["Alabama", "Georgia"],
            "away_team": ["LSU", "Tennessee"],
            "neutral_site": [False, False],
        }
    )

    matrix = prepare_schedule(df)

    assert list(matrix.columns) == [0, 1, 2]
    assert matrix.loc["Alabama", 0] == "H"
    assert matrix.loc["LSU", 0] == "A"
    assert (matrix[1] == "BYE").all()


def test_invalid_schedule():
    df = pd.DataFrame(
        {
            "week": [-1],
            "home_team": ["Alabama"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    with pytest.raises(ValueError):
        prepare_schedule(df)


def test_input_unchanged():
    df = pd.DataFrame(
        {
            "week": [1],
            "home_team": ["Alabama"],
            "away_team": ["LSU"],
            "neutral_site": [False],
        }
    )

    original = df.copy(deep=True)

    prepare_schedule(df)

    assert_frame_equal(df, original)
