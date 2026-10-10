from cfb_viz.validation import validate_schedule
import pandas as pd
import numpy as np


def prepare_schedule(df):
    validate_schedule(df)

    home_games = df[["week", "home_team", "away_team", "neutral_site"]].rename(
        columns={
            "home_team": "team",
            "away_team": "opponent",
        }
    )
    home_games["location"] = np.where(home_games["neutral_site"], "N", "H")

    away_games = df[["week", "away_team", "home_team", "neutral_site"]].rename(
        columns={
            "away_team": "team",
            "home_team": "opponent",
        }
    )
    away_games["location"] = np.where(away_games["neutral_site"], "N", "A")

    team_schedule = pd.concat([home_games, away_games], axis=0, ignore_index=True).drop(
        columns=["neutral_site"]
    )

    min_week = team_schedule["week"].min()
    max_week = team_schedule["week"].max()

    schedule_matrix = team_schedule.pivot(
        index="team", columns="week", values="location"
    )
    schedule_matrix = schedule_matrix.reindex(
        columns=range(min_week, max_week + 1), fill_value="BYE"
    ).fillna("BYE")

    return schedule_matrix
