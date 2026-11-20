import sys

import pytest

from trackio.cli import main


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        (
            "freeze",
            "Not supported. Static Spaces serve their data publicly, so a frozen snapshot cannot be private. Use a Gradio Space for a private dashboard.",
        ),
        ("sync", "Not supported with --sdk static."),
    ],
)
def test_private_help_explains_static_space_limitation(
    command, expected, monkeypatch, capsys
):
    monkeypatch.setattr(sys, "argv", ["trackio", command, "--help"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    output = " ".join(capsys.readouterr().out.split())
    assert expected in output
