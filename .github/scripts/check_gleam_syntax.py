"""Check syntax of a Gleam golden file using ``gleam check``."""

from _gleam_fixture import run_gleam_subcommand


def main() -> None:
    """Check syntax of the given Gleam golden file."""
    run_gleam_subcommand(subcommand="check")


if __name__ == "__main__":
    main()
