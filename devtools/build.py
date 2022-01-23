import subprocess
import sys
from typing import NoReturn

import toml

# some colors for terminal output
CRED = "\33[31m"
CGREEN = "\33[32m"
CWHITE = "\33[97m"
CEND = "\33[0m"


def fail(header: str, message: str = "") -> NoReturn:
    print(f"\n\n{CRED}{header}{CEND}\n{message}\n\n")
    sys.exit(1)


def run_commands(commands: list[str], message_on_fail: str = "Aborted: Command failed") -> None:
    for command in commands:
        print(command)
        result = subprocess.run(command, shell=True, check=False)
        if result.returncode != 0:
            fail(f"{message_on_fail}", "Failed command: " + command)


def check() -> None:
    batch = [
        "pytest",
        "black --check poetry_example tests",
        "mypy poetry_example tests",
        "pylint --fail-under=9 poetry_example tests",
    ]
    run_commands(batch, message_on_fail="Checks failed!")


def docker() -> None:
    check()

    pyproject = toml.load("pyproject.toml")
    project_version = pyproject["tool"]["poetry"]["version"]

    docker_version = f"poetry_example/example:{project_version}"
    batch = [
        "poetry build",
        "poetry run poetry-lock-package --build",
        "docker run --rm --privileged multiarch/qemu-user-static --reset -p yes ",
        f"env DOCKER_BUILDKIT=1 docker build --no-cache --platform=linux/arm64 -t {docker_version} .",
    ]
    print(f"Building docker container {docker_version}")
    run_commands(batch, message_on_fail="Failed to build Docker container")


def release() -> None:
    pyproject = toml.load("pyproject.toml")

    #
    # Sanity checks
    #

    # check if repo is clean
    print("Checking if repository is clean")
    result = subprocess.run("git status --porcelain", shell=True, stdout=subprocess.PIPE, check=False)
    if result.stdout != b"":
        fail("Release aborted: Working Directory is not clean", "Offending files:\n" + result.stdout.decode("UTF-8"))

    # check project version
    print("Checking versions")
    version = pyproject["tool"]["poetry"]["version"]
    if not version.endswith(".dev"):
        fail("Release aborted: Not on a .dev version", f"Detected version is {version}")

    # check no .dev dependencies
    for dep_name, dep_version in pyproject["tool"]["poetry"]["dependencies"].items():
        if ".dev" in dep_version:
            fail(
                "Release aborted: the project must not have any .dev dependencies",
                f"but found {dep_name}:{dep_version}",
            )

    # check code
    check()

    #
    # Release
    #

    # ask if user is sure
    release_version = version.replace(".dev", "")
    print(f"\n{CGREEN}Checks succeded{CEND}\n")
    response = input(f"Are you sure you want to create release {CWHITE}{release_version}{CEND} (y/N):")
    if response.lower() != "y":
        fail("Release Cancelled")

    # tag the release version
    print(f"Tagging release {release_version}")
    commands = [
        f"poetry version {release_version}",
        "git add pyproject.toml",
        f"""git commit -m"set release version to {release_version}" """,
        f"""git tag -a {release_version} -m "Tagged release {release_version}" """,
    ]
    run_commands(commands, message_on_fail="Release aborted: Failed to tag the release")

    # start next dev version
    version_parts = [int(x) for x in release_version.split(".")]
    version_parts[2] += 1
    new_version = ".".join(str(x) for x in version_parts) + ".dev"

    print(f"Starting next dev version: {new_version}")
    commands = [
        f"poetry version {new_version}",
        "git add pyproject.toml",
        f"""git commit -m"start developing version {new_version}" """,
    ]
    run_commands(commands, message_on_fail="Release aborted: Failed to start new dev version")

    print("\n\n")
    print(
        f"{CGREEN}Release done{CEND}. Run {CWHITE}git push origin master {release_version}{CEND} to make it permanent!"
    )
    print("\n")


def doc() -> None:
    """ Build Sphinx documentation """
    batch = [
        "sphinx-build -M clean doc/source doc/build",
        "sphinx-build -M html  doc/source doc/build",
        "sphinx-build -M latexpdf doc/source doc/build",
    ]

    run_commands(batch, message_on_fail="Failed to build the documentation.")


if __name__ == "__main__":
    # Why does this main exist, when we have Poe?
    # In perfect world the tasks in this file would all be called directly by poe. But poe currently does not work well
    # on Windows. This main is here to allow running the build tasks from the Windows commandline like so:
    #    python -m devtools.build doc

    cmd = sys.argv[1]
    if cmd == "doc":
        doc()
    elif cmd == "release":
        release()
    elif cmd == "docker":
        docker()
    elif cmd == "check":
        check()
    else:
        raise ValueError(f"Unknown command: {cmd}")
