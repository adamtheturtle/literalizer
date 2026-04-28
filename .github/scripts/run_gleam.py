"""Run a Gleam golden file using ``gleam run``."""

from _gleam_fixture import run_gleam_subcommand


def main() -> None:
    """Run the given Gleam golden file."""
    run_gleam_subcommand(subcommand="run")


if __name__ == "__main__":
    main()
