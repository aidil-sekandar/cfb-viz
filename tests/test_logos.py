import pytest
from PIL import Image

from cfb_viz.logos import get_team_logo


def test_get_team_logo_returns_image():
    logo = get_team_logo("Alabama Crimson Tide")

    assert isinstance(logo, Image.Image)


def test_get_team_logo_has_valid_dimensions():
    logo = get_team_logo("Alabama Crimson Tide")

    width, height = logo.size

    assert width > 0
    assert height > 0


def test_get_team_logo_preserves_transparency():
    logo = get_team_logo("Alabama Crimson Tide")

    assert logo.mode == "RGBA"


def test_get_team_logo_multiple_teams():
    teams = [
        "Alabama Crimson Tide",
        "Georgia Bulldogs",
        "Texas Longhorns",
    ]

    for team in teams:
        logo = get_team_logo(team)

        assert isinstance(logo, Image.Image)
        assert logo.width > 0
        assert logo.height > 0


def test_get_team_logo_invalid_team():
    with pytest.raises(ValueError, match="not found"):
        get_team_logo("Nonexistent University")


def test_get_team_logo_missing_file(monkeypatch, tmp_path):
    import cfb_viz.logos as logos_module

    # Simulate an existing team whose logo file is missing.
    monkeypatch.setattr(
        logos_module,
        "get_team",
        lambda name: {"team_id": "missing-logo"},
    )

    # Redirect package resource lookup to a temporary directory.
    monkeypatch.setattr(
        logos_module,
        "files",
        lambda package: tmp_path,
    )

    with pytest.raises(FileNotFoundError, match="Logo not found"):
        get_team_logo("Missing Logo University")


def test_get_team_logo_image_remains_usable():
    logo = get_team_logo("Alabama Crimson Tide")

    # Verify the image data is accessible after the file is closed.
    pixels = logo.tobytes()

    assert len(pixels) > 0
