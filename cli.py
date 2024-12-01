import subprocess


def clean(files: list[str] = ["."]) -> None:
    """
    Clean up the code by running several code quality tools.

    This function runs the following tools on the specified files or directories:
    1. autoflake: Removes all unused imports and unused variables.
    2. isort: Sorts imports according to the "black" profile.
    3. black: Formats the code according to the Black code style.
    4. mypy: Performs static type checking.

    Args:
        files (list[str]): A list of file or directory paths to clean. Defaults to the current directory.
    """
    subprocess.run(
        [
            "autoflake",
            "-r",
            "--exclude=__init__.py",
            "--remove-all-unused-imports",
            "--remove-unused-variables",
            "-i",
            *files,
        ]
    )
    subprocess.run(["isort", *files, "--profile", "black"])
    subprocess.run(["black", *files])
    subprocess.run(["mypy", *files])


if __name__ == "__main__":
    clean()
