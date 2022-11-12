import functools
from collections.abc import Sequence

import pytest
from click.testing import Result
from typer.testing import CliRunner

from kip.main import app


class KipCliRunner(CliRunner):
    def invoke_config(self, args: Sequence[str]) -> Result:
        return self.invoke(app, ["config", *args])

    def invoke_base(self, args: Sequence[str], user_input: str | None = None) -> Result:
        return self.invoke(app, args, input=user_input)


@pytest.fixture
def runner() -> KipCliRunner:
    return KipCliRunner()
