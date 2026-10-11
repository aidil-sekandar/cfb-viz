from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Literal
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from cfb_viz.logos import get_team_logo

from cfb_viz.schedule import _to_team_schedule, _to_matrix
from cfb_viz.teams import get_team_mapping

location_codes = {
    "H": 0,
    "A": 1,
    "N": 2,
    "BYE": 3,
}

default_colors = {
    "H": "#ffffff",
    "A": "#f8e6c7",
    "N": "#c9dec4",
    "BYE": "#dedfe1",
}

color_order = ["H", "A", "N", "BYE"]


def plot_schedule(
    df: pd.DataFrame,
    figsize: tuple[float, float] | None = None,
    colors: dict[str, str] | None = None,
    opponent_display: Literal["full", "short", "abbreviation", "logo"] = "full",
) -> tuple[Figure, Axes]:
    team_schedule = _to_team_schedule(df)

    location_matrix = _to_matrix(team_schedule, "location")
    opponent_matrix = _to_matrix(team_schedule, "opponent")

    if opponent_display in ("short", "abbreviation"):
        opponent_matrix = opponent_matrix.replace(get_team_mapping(opponent_display))
    elif opponent_display not in ("full", "logo"):
        raise ValueError(f"Invalid opponent display: '{opponent_display}'")

    use_logos = opponent_display == "logo"

    n_teams, n_weeks = location_matrix.shape
    default_figsize = (max(8, n_weeks * 1.5), max(4, n_teams * 0.9))

    if figsize is None:
        figsize = default_figsize

    fig, ax = plt.subplots(figsize=figsize)

    color_matrix = location_matrix.replace(location_codes)
    color_matrix = color_matrix.astype(int)

    if colors is None:
        colors = default_colors
    else:
        colors = default_colors | colors

    cmap = ListedColormap([colors[key] for key in color_order])

    sns.heatmap(
        color_matrix,
        ax=ax,
        cmap=cmap,  # color map
        vmin=0,
        vmax=3,
        cbar=False,  # disable color bar
        annot=False if use_logos else opponent_matrix,
        fmt="s",  # format annotation as string
        linewidths=1.5,
        linecolor="black",
    )

    if use_logos:
        for row_index, team_name in enumerate(opponent_matrix.index):
            for col_index, week in enumerate(opponent_matrix.columns):
                opponent = opponent_matrix.loc[team_name, week]

                if opponent == "BYE":  # type: ignore
                    continue

                x = col_index + 0.5
                y = row_index + 0.5

                logo = get_team_logo(opponent)  # type: ignore

                image = OffsetImage(logo, zoom=0.15)  # type: ignore

                annotation = AnnotationBbox(
                    image,
                    (x, y),
                    frameon=False,
                )

                ax.add_artist(annotation)

    ax.xaxis.tick_top()
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("College Football Schedule Matrix", pad=30)

    print("\nopponent:\n", opponent_matrix)
    print("\nlocation:\n", location_matrix)
    print("\ncolor matrix:\n", color_matrix)

    return fig, ax
