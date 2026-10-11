import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest  # type: ignore

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.colors import to_rgba

from cfb_viz.plotting import plot_schedule


@pytest.fixture
def sample_schedule():
    return pd.DataFrame(
        {
            "week": [1, 1, 2, 2, 3],
            "home_team": [
                "Alabama",
                "Georgia",
                "LSU",
                "Alabama",
                "Georgia",
            ],
            "away_team": [
                "LSU",
                "Auburn",
                "Georgia",
                "Auburn",
                "Alabama",
            ],
            "neutral_site": [False, False, False, False, True],
        }
    )


def test_plot_schedule_returns_figure_and_axes(sample_schedule):
    fig, ax = plot_schedule(sample_schedule)

    try:
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)
    finally:
        plt.close(fig)


def test_plot_schedule_default_figsize(sample_schedule):
    fig, ax = plot_schedule(sample_schedule)

    try:
        assert tuple(fig.get_size_inches()) == pytest.approx((8, 4))
    finally:
        plt.close(fig)


def test_plot_schedule_custom_figsize(sample_schedule):
    fig, ax = plot_schedule(sample_schedule, figsize=(12, 6))

    try:
        assert tuple(fig.get_size_inches()) == pytest.approx((12, 6))
    finally:
        plt.close(fig)


def test_plot_schedule_default_colors(sample_schedule):
    fig, ax = plot_schedule(sample_schedule)

    try:
        cmap = ax.collections[0].cmap

        assert cmap(0.0) == to_rgba("#ffffff")
        assert cmap(1 / 3) == to_rgba("#f8e6c7")
        assert cmap(2 / 3) == to_rgba("#c9dec4")
        assert cmap(1.0) == to_rgba("#dedfe1")
    finally:
        plt.close(fig)


def test_plot_schedule_partial_color_override(sample_schedule):
    fig, ax = plot_schedule(
        sample_schedule,
        colors={"H": "#0032A0"},
    )

    try:
        cmap = ax.collections[0].cmap

        assert cmap(0.0) == to_rgba("#0032A0")
        assert cmap(1 / 3) == to_rgba("#f8e6c7")
        assert cmap(2 / 3) == to_rgba("#c9dec4")
        assert cmap(1.0) == to_rgba("#dedfe1")
    finally:
        plt.close(fig)


def test_plot_schedule_opponent_annotations(sample_schedule):
    fig, ax = plot_schedule(sample_schedule)

    try:
        annotations = [text.get_text() for text in ax.texts]

        assert len(annotations) == 12  # 4 teams × 3 weeks
        assert "LSU" in annotations
        assert "Georgia" in annotations
        assert "BYE" in annotations
    finally:
        plt.close(fig)


def test_plot_schedule_does_not_mutate_input(sample_schedule):
    original = sample_schedule.copy(deep=True)

    fig, ax = plot_schedule(sample_schedule)

    try:
        pd.testing.assert_frame_equal(sample_schedule, original)
    finally:
        plt.close(fig)


@pytest.fixture
def ncaa_schedule():
    return pd.DataFrame(
        {
            "week": [1, 2],
            "home_team": [
                "Alabama Crimson Tide",
                "Virginia Cavaliers",
            ],
            "away_team": [
                "Virginia Cavaliers",
                "Alabama Crimson Tide",
            ],
            "neutral_site": [False, False],
        }
    )


def get_annotations(ax):
    return [text.get_text() for text in ax.texts]


def test_opponent_display_full(ncaa_schedule):
    fig, ax = plot_schedule(ncaa_schedule, opponent_display="full")

    try:
        annotations = get_annotations(ax)

        assert "Alabama Crimson Tide" in annotations
        assert "Virginia Cavaliers" in annotations
    finally:
        plt.close(fig)


def test_opponent_display_short(ncaa_schedule):
    fig, ax = plot_schedule(ncaa_schedule, opponent_display="short")

    try:
        annotations = get_annotations(ax)

        assert "Alabama" in annotations
        assert "Virginia" in annotations

        assert "Alabama Crimson Tide" not in annotations
        assert "Virginia Cavaliers" not in annotations
    finally:
        plt.close(fig)


def test_opponent_display_abbreviation(ncaa_schedule):
    fig, ax = plot_schedule(
        ncaa_schedule,
        opponent_display="abbreviation",
    )

    try:
        annotations = get_annotations(ax)

        assert "ALA" in annotations
        assert "UVA" in annotations
    finally:
        plt.close(fig)


def test_opponent_display_default(ncaa_schedule):
    fig, ax = plot_schedule(ncaa_schedule)

    try:
        annotations = get_annotations(ax)

        assert "Alabama Crimson Tide" in annotations
        assert "Virginia Cavaliers" in annotations
    finally:
        plt.close(fig)


@pytest.mark.parametrize("display", ["logo", "invalid", "SHORT", None])
def test_opponent_display_invalid(ncaa_schedule, display):
    with pytest.raises(ValueError, match="Invalid opponent display"):
        fig, _ = plot_schedule(
            ncaa_schedule,
            opponent_display=display,
        )
        plt.close(fig)


def test_opponent_display_does_not_mutate_dataframe(ncaa_schedule):
    original = ncaa_schedule.copy(deep=True)

    fig, _ = plot_schedule(
        ncaa_schedule,
        opponent_display="short",
    )

    try:
        pd.testing.assert_frame_equal(ncaa_schedule, original)
    finally:
        plt.close(fig)
