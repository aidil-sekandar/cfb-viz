import pandas as pd
import pytest  # type: ignore

from cfb_viz.teams import load_teams
from cfb_viz.teams import get_team
from cfb_viz.teams import get_team_mapping

EXPECTED_COLUMNS = [
    "team_id",
    "school_name",
    "mascot",
    "short_name",
    "ncaa_name",
    "espn_abbreviation",
]


def test_load_teams_returns_dataframe():
    teams = load_teams()

    assert isinstance(teams, pd.DataFrame)


def test_load_teams_has_expected_columns():
    teams = load_teams()

    assert list(teams.columns) == EXPECTED_COLUMNS


def test_load_teams_has_138_teams():
    teams = load_teams()

    assert len(teams) == 138


def test_load_teams_has_unique_ids():
    teams = load_teams()

    assert teams["team_id"].is_unique


def test_load_teams_has_unique_ncaa_names():
    teams = load_teams()

    assert teams["ncaa_name"].is_unique


def test_load_teams_has_no_missing_values():
    teams = load_teams()

    assert not teams[EXPECTED_COLUMNS].isna().any().any()


def test_load_teams_contains_alabama():
    teams = load_teams()

    alabama = teams.loc[teams["team_id"] == "alabama"]

    assert len(alabama) == 1
    assert alabama.iloc[0]["ncaa_name"] == "Alabama Crimson Tide"
    assert alabama.iloc[0]["short_name"] == "Alabama"


def test_get_team_returns_dictionary():
    team = get_team("Alabama Crimson Tide")

    assert isinstance(team, dict)


def test_get_team_returns_correct_metadata():
    team = get_team("Alabama Crimson Tide")

    assert team == {
        "team_id": "alabama",
        "school_name": "University of Alabama",
        "mascot": "Crimson Tide",
        "short_name": "Alabama",
        "ncaa_name": "Alabama Crimson Tide",
        "espn_abbreviation": "ALA",
    }


def test_get_team_different_team():
    team = get_team("Virginia Cavaliers")

    assert team["team_id"] == "virginia"
    assert team["short_name"] == "Virginia"
    assert team["mascot"] == "Cavaliers"


def test_get_team_has_all_columns():
    team = get_team("Syracuse Orange")

    expected_keys = {
        "team_id",
        "school_name",
        "mascot",
        "short_name",
        "ncaa_name",
        "espn_abbreviation",
    }

    assert set(team.keys()) == expected_keys


def test_get_team_invalid_name():
    with pytest.raises(ValueError):
        get_team("Nonexistent University")


def test_get_team_requires_exact_name():
    with pytest.raises(ValueError):
        get_team("Virginia")


def test_get_team_case_sensitive():
    with pytest.raises(ValueError):
        get_team("alabama crimson tide")


def test_get_team_empty_string():
    with pytest.raises(ValueError):
        get_team("")


def test_get_team_error_message():
    with pytest.raises(
        ValueError,
        match="Team 'Unknown Team' not found",
    ):
        get_team("Unknown Team")


def test_team_mapping_short():
    mapping = get_team_mapping("short")

    assert isinstance(mapping, dict)
    assert mapping["Alabama Crimson Tide"] == "Alabama"
    assert mapping["Virginia Cavaliers"] == "Virginia"


def test_team_mapping_abbreviation():
    mapping = get_team_mapping("abbreviation")

    assert mapping["Alabama Crimson Tide"] == "ALA"
    assert mapping["Virginia Cavaliers"] == "UVA"


def test_team_mapping_contains_all_teams():
    mapping = get_team_mapping("short")

    assert len(mapping) == 138


def test_team_mapping_invalid_display():
    with pytest.raises(ValueError, match="Invalid display option"):
        get_team_mapping("logo")


def test_team_mapping_does_not_modify_metadata():
    before = load_teams()
    get_team_mapping("short")
    after = load_teams()

    pd.testing.assert_frame_equal(before, after)
