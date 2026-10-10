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


def plot_schedule(df):
    team_schedule = _to_team_schedule(df)

    location_matrix = _to_matrix(team_schedule, "location")
    opponent_matrix = _to_matrix(team_schedule, "opponent")

    color_matrix = location_matrix.replace(location_codes)
    color_matrix = color_matrix.astype(int)

    cmap = ListedColormap(["#ffffff", "#f8e6c7", "#c9dec4", "#dedfe1"])

    fig, ax = plt.subplots(figsize=(10, 5))

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
