from kip.base import app as base_app
from kip.config import app as config_app

app = base_app
app.add_typer(config_app, name="config")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
