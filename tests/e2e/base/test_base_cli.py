from e2e.conftest import KipCliRunner


def test_list_command(runner: KipCliRunner) -> None:
    result = runner.invoke_base(["list"])
    assert result.exit_code == 0
