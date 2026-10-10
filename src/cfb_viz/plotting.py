import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap

from cfb_viz.schedule import _to_team_schedule, _to_matrix

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


def plot_schedule(df, figsize=None, colors=None):
    team_schedule = _to_team_schedule(df)

    location_matrix = _to_matrix(team_schedule, "location")
    opponent_matrix = _to_matrix(team_schedule, "opponent")

    n_teams, n_weeks = location_matrix.shape
    default_figsize = (max(8, n_weeks * 1.5), max(4, n_teams * 0.6))

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
        annot=opponent_matrix,  # annotate the cells with opponents name
        fmt="s",  # format annotation as string
        linewidths=1.5,
        linecolor="black",
    )

    ax.xaxis.tick_top()
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("College Football Schedule Matrix", pad=30)

    print("\nopponent:\n", opponent_matrix)
    print("\nlocation:\n", location_matrix)
    print("\ncolor matrix:\n", color_matrix)

    return fig, ax
