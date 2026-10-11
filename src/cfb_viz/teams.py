import pandas as pd
from importlib.resources import files


def load_teams() -> pd.DataFrame:
    csv_resource = files("cfb_viz.data").joinpath("teams.csv")
    fbs_teams = pd.read_csv(csv_resource)  # type: ignore

    return fbs_teams


def get_team(ncaa_name: str) -> dict:
    fbs_teams = load_teams()

    requested_team = fbs_teams.loc[fbs_teams["ncaa_name"] == ncaa_name]

    if requested_team.empty:
        raise ValueError(f"Team '{ncaa_name}' not found.")

    return requested_team.iloc[0].to_dict()


def get_team_mapping(display: str) -> dict[str, str]:
    fbs_teams = load_teams()

    if display == "short":
        column = "short_name"
    elif display == "abbreviation":
        column = "espn_abbreviation"
    else:
        raise ValueError(f"Invalid display option: '{display}'")

    mapping = fbs_teams.set_index("ncaa_name")[column].to_dict()
    return {str(key): str(value) for key, value in mapping.items()}
