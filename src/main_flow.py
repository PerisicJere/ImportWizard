# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path

from flow_compose import flow, Flow
import sys

from compare_poetry_and_imports import poetry_flow
from compare_venv_and_imports import venv_flow
from read_impwiz_files import used_imports_flow

target_folder =  Path.cwd()


@flow(
    used_imports_flow=Flow(used_imports_flow),
    poetry_flow=Flow(poetry_flow),
)
def main_flow()->None:
    arguments = sys.argv[1:]
    if '--requirements' in arguments or '-r' in arguments:
        used_imports_flow(target_folder=target_folder)
    elif '--poetry' in arguments or '-p' in arguments:
        if '--difference' in arguments or '-d' in arguments:
            poetry_flow(target_folder=target_folder, set_function="-d")
        elif '--intersection' in arguments or '-i' in arguments:
            poetry_flow(target_folder=target_folder, set_function="-i")
    elif '--venv' in arguments:
        venv_flow()
    elif '--help' in arguments or '-h' in arguments:
        print("""
Usage: impwiz [OPTIONS]

Options:
  -r, --requirements        Generate requirements.txt from used imports
  -p, --poetry              Use poetry.lock / pyproject.toml as dependency source
  -d, --difference          Show declared dependencies not used in code
  -i, --intersection        Show used imports that are in poetry.lock
  --venv                    Show imports in virtual environment
  -h, --help                Show this help message
""".strip())
    else:
        print("Unknown command. Try impwiz --help")

if __name__ == '__main__':
    main_flow()