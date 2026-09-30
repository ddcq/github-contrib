from github_contrib import svg


def test_palette_locked():
    assert svg.PALETTE["NONE"] == "#eff2f5"
    assert svg.PITCH == 13
