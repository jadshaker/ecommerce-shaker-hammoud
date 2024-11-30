import subprocess


def clean(files: list[str] = ["."]) -> None:
    """
    command: clean
    Clean up the code
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
