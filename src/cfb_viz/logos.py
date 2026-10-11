from importlib.resources import files
from PIL import Image

from cfb_viz.teams import get_team


def get_team_logo(ncaa_name: str) -> Image.Image:  # type: ignore
    team = get_team(ncaa_name)

    team_id = team["team_id"]
    filename = f"{team_id}.png"

    logo_resource = files("cfb_viz").joinpath("assets", "logos", filename)

    if not logo_resource.is_file():
        raise FileNotFoundError(f"Logo not found for '{ncaa_name}'")

    with logo_resource.open("rb") as file:
        image = Image.open(file)
        logo = image.copy()

    return logo
