# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import io
from contextlib import redirect_stdout
from pathlib import Path
from typing import Set

import tomlkit
from pandas.compat import set_function_name

from constants import SOURCE_FOLDER, FILE_EXTENSION
import subprocess
from flow_compose import flow, flow_function, FlowFunction, FlowArgument

from read_impwiz_files import main_flow


@flow_function(cached=True)
def get_used_imports(target_folder: FlowFunction[str] = None) -> set[str]:
    used_imports: set[str] = set()
    f = io.StringIO()
    with redirect_stdout(f):
        main_flow(target_folder = Path(target_folder()) if target_folder else SOURCE_FOLDER)
    used_imports.add(f.getvalue().replace("\n", ""))
    return used_imports

@flow_function(cached=True)
def find_poetry_lock_files(target_folder: FlowFunction[str] = None) -> list[Path]:
    folder_to_use = Path(target_folder()) if target_folder else SOURCE_FOLDER
    poetry_lock_files: list[Path] = [
        file
        for file in folder_to_use.rglob("poetry.lock")
    ]
    return poetry_lock_files

@flow_function(cached=True)
def parse_poetry_lock(poetry_lock_files: FlowFunction[list[Path]]) -> dict[str, str]:
    dependencies: dict[str, str] = dict()
    for poetry_lock_file in poetry_lock_files():
        with poetry_lock_file.open() as f:
            poetry_lock = tomlkit.parse(f.read())
            for i in range(len(poetry_lock['package'])):
                dependencies[poetry_lock['package'][i]['name']] = poetry_lock['package'][i]['version']
                if 'dependencies' in poetry_lock['package'][i]:
                    for dependency, version in poetry_lock['package'][i]['dependencies'].items():
                        if isinstance(version, str):
                            dependencies[dependency] = version

    return dependencies

@flow_function(cached=True)
def set_from_dict(parse_poetry_lock: FlowFunction[list[Path]]) -> set[str]:
    dependencies: set[str] = set()
    for dependency, version in parse_poetry_lock().items():
        if version.startswith('<=') or version.startswith('>='):
            dependencies.add(f"{dependency}{version}")
        else:
            dependencies.add(f"{dependency}=={version}")

    return dependencies

@flow_function(cached=True)
def difference_of_used_imports_and_dependencies(dependencies_set: FlowFunction[set[str]], used_imports: FlowFunction[set[str]]) -> \
None:
    used_imports: set[str] = used_imports()
    dependencies: set[str] = dependencies_set()
    difference = list(dependencies.difference(used_imports))

    for dif in sorted(difference):
        print(dif)

@flow_function(cached=True)
def intersection_of_used_imports_and_dependencies(dependencies_set: FlowFunction[set[str]], used_imports: FlowFunction[set[str]]) -> \
None:
    used_imports: set[str] = used_imports()
    dependencies: set[str] = dependencies_set()
    intersection = list(dependencies.intersection(used_imports))
    for inter in sorted(intersection):
        print(inter)

@flow_function(cached=True)
def choose_set_function(difference: FlowFunction[None], intersection: FlowFunction[None], set_function: FlowArgument[str]) -> None:
    if set_function() in {"--difference", "-d"}:
        difference()
    elif set_function() in {"--intersection", "-i"}:
        intersection()
    else:
        assert set_function() in ["difference", "intersection"], "Invalid function choice"


@flow(
    target_folder=FlowArgument(str, default=str(SOURCE_FOLDER)),
    set_function=FlowArgument(str, default="--difference"),
    used_imports=get_used_imports,
    poetry_lock_files=find_poetry_lock_files,
    parse_poetry_lock=parse_poetry_lock,
    dependencies_set=set_from_dict,
    difference=difference_of_used_imports_and_dependencies,
    intersection=intersection_of_used_imports_and_dependencies,
    choose_set_function=choose_set_function
)
def poetry_flow(choose_set_function: FlowFunction[None]) -> None:
    choose_set_function()
