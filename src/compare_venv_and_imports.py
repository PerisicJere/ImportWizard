# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flow_compose import flow, flow_function, FlowFunction
import subprocess

@flow_function(cached=True)
def get_dict_of_dependencies() -> dict[str, str]:
    dependencies: dict[str, str] = {}
    venv_info = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    if venv_info.returncode == 0:
        for line in venv_info.stdout.split('\n')[2:]:
            name_and_version = line.split(" ")
            if len(name_and_version) > 2:
                dependencies[name_and_version[0].strip()] = name_and_version[-1].strip()
    return dependencies

@flow_function(cached=True)
def display_from_dict(dict_of_dependencies: FlowFunction[dict[str, str]]) -> None:
    for name, version in dict_of_dependencies().items():
        print(f"{name}=={version}")

@flow(
    dict_of_dependencies=get_dict_of_dependencies,
    venv_dependencies=display_from_dict
)
def venv_flow(venv_dependencies: FlowFunction[None]) -> None:
    venv_dependencies()

if __name__ == '__main__':
    venv_flow()
