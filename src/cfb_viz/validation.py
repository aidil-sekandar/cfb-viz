import pandas as pd

required_columns = {"week", "home_team", "away_team", "neutral_site"}


def validate_schedule(df):
    # check for valid Pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame")

    # check for any missing columns
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # check for week's validity (+ integer)
    if (
        not pd.api.types.is_integer_dtype(df["week"])
        or not (df["week"] > 0).all()
        or df["week"].isna().any()
    ):
        raise ValueError("week must contain positive integers")

    # check for team's name validity
    for column in ["home_team", "away_team"]:
        if not all(isinstance(name, str) and bool(name.strip()) for name in df[column]):
            raise ValueError("team name must contain nonempty strings")

    # check if any teams playing against itself
    if (df["home_team"] == df["away_team"]).any():
        raise ValueError("A team cannot play against itself")

    # check if neutral_site contains only boolean type
    if (
        not pd.api.types.is_bool_dtype(df["neutral_site"])
        or df["neutral_site"].isna().any()
    ):
        raise ValueError("neutral_site must contain boolean values")

    # check for duplicated rows(matches)
    if df.duplicated(subset=["week", "home_team", "away_team"]).any():
        raise ValueError("Duplicate games detected")

    home = df[["week", "home_team"]].rename(columns={"home_team": "team"})
    away = df[["week", "away_team"]].rename(columns={"away_team": "team"})

    # check if any teams playing twice a week
    all_teams = pd.concat([home, away], ignore_index=True)
    if all_teams.duplicated(subset=["week", "team"]).any():
        raise ValueError("A team cannot play multiple games in the same week")
