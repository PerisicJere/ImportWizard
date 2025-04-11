# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flow_compose import flow, flow_function, FlowFunction, FlowArgument
import subprocess

from compare_poetry_and_imports import get_used_imports
from constants import SOURCE_FOLDER
from utils import (
    difference_of_used_imports_and_dependencies,
    intersection_of_used_imports_and_dependencies,
)


@flow_function(cached=True)
def get_dict_of_dependencies() -> dict[str, str]:
    dependencies: dict[str, str] = {}
    venv_info = subprocess.run(["pip", "list"], capture_output=True, text=True)
    if venv_info.returncode == 0:
        for line in venv_info.stdout.split("\n")[2:]:
            name_and_version = line.split(" ")
            if len(name_and_version) > 2:
                dependencies[name_and_version[0].strip()] = name_and_version[-1].strip()
    return dependencies


@flow_function(cached=True)
def dict_to_set_venv(dict_of_dependencies: FlowFunction[dict[str, str]]) -> set[str]:
    dependencies: set[str] = set()
    for name, version in dict_of_dependencies().items():
        dependencies.add(f"{name}=={version}")
    return dependencies


@flow_function(cached=True)
def display_with_set_functions_venv(
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
        assert dependencies_set() is not None, (
            "There is no dependencies, or failed to find venv. Command: impwiz --venv [-a | --all]"
        )
        for dependency in sorted(dependencies_set()):
            print(dependency)
    else:
        assert set_function() in ["--difference", "--intersection", "--all"], (
            "Invalid function choice"
        )


@flow(
    target_folder=FlowArgument(str, default=str(SOURCE_FOLDER)),
    set_function=FlowArgument(str, default="--difference"),
    used_imports=get_used_imports,
    dict_of_dependencies=get_dict_of_dependencies,
    dependencies_set=dict_to_set_venv,
    venv_dependencies=display_with_set_functions_venv,
)
def venv_flow(venv_dependencies: FlowFunction[None]) -> None:
    venv_dependencies()
