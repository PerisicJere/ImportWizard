# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import io
from contextlib import redirect_stdout
from pathlib import Path
import tomlkit
from flow_compose import flow, flow_function, FlowFunction, FlowArgument

from constants import SOURCE_FOLDER
from read_impwiz_files import used_imports_flow
from utils import (
    difference_of_used_imports_and_dependencies,
    intersection_of_used_imports_and_dependencies,
)


@flow_function(cached=True)
def get_used_imports(target_folder: FlowFunction[str] = None) -> set[str]:
    used_imports: set[str] = set()
    f = io.StringIO()
    with redirect_stdout(f):
        used_imports_flow(
            target_folder=Path(target_folder()) if target_folder else SOURCE_FOLDER
        )
    for line in f.getvalue().splitlines():
        used_imports.add(line)
    return used_imports


@flow_function(cached=True)
def find_poetry_lock_files(target_folder: FlowFunction[str] = None) -> list[Path]:
    folder_to_use = Path(target_folder()) if target_folder else SOURCE_FOLDER
    poetry_lock_files: list[Path] = [
        file for file in folder_to_use.rglob("poetry.lock")
    ]
    return poetry_lock_files


@flow_function(cached=True)
def parse_poetry_lock(poetry_lock_files: FlowFunction[list[Path]]) -> dict[str, str]:
    dependencies: dict[str, str] = dict()
    for poetry_lock_file in poetry_lock_files():
        with poetry_lock_file.open() as f:
            poetry_lock = tomlkit.parse(f.read())
            for i in range(len(poetry_lock["package"])):
                dependencies[poetry_lock["package"][i]["name"]] = poetry_lock[
                    "package"
                ][i]["version"]
                if "dependencies" in poetry_lock["package"][i]:
                    for dependency, version in poetry_lock["package"][i][
                        "dependencies"
                    ].items():
                        if isinstance(version, str):
                            dependencies[dependency] = version

    return dependencies


@flow_function(cached=True)
def set_from_dict(parsed_poetry_lock_dict: FlowFunction[list[Path]]) -> set[str]:
    dependencies: set[str] = set()
    for dependency, version in parsed_poetry_lock_dict().items():
        if version.startswith("<=") or version.startswith(">="):
            dependencies.add(f"{dependency}{version}")
        else:
            dependencies.add(f"{dependency}=={version}")

    return dependencies


@flow_function(cached=True)
def display_with_set_functions_poetry(
    dependencies_set: FlowFunction[set[str]],
    used_imports: FlowFunction[set[str]],
    set_function: FlowArgument[str],
) -> None:
    if set_function() in {"--difference", "-d"}:
        difference_of_used_imports_and_dependencies(
            dependencies_set=dependencies_set(), used_imports=used_imports()
        )
    elif set_function() in {"--intersection", "-i"}:
        intersection_of_used_imports_and_dependencies(
            dependencies_set=dependencies_set(), used_imports=used_imports()
        )
    elif set_function() in {"--all", "-a"}:
        for dependency in dependencies_set():
            print(dependency)
    else:
        assert set_function() in ["--difference", "--intersection", "--all"], (
            "Invalid function choice"
        )


@flow(
    target_folder=FlowArgument(str, default=str(SOURCE_FOLDER)),
    set_function=FlowArgument(str, default="--difference"),
    used_imports=get_used_imports,
    poetry_lock_files=find_poetry_lock_files,
    parsed_poetry_lock_dict=parse_poetry_lock,
    dependencies_set=set_from_dict,
    display_dependencies=display_with_set_functions_poetry,
)
def poetry_flow(display_dependencies: FlowFunction[None]) -> None:
    display_dependencies()
