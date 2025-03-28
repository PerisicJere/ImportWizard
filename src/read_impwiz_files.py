# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os.path
from pathlib import Path
from constants import FILES_TO_SKIP, SOURCE_FOLDER, FILE_EXTENSION, IMPORT_REGEX, REQ_FILE, FROM_IMPORT_REGEX
import subprocess
from import_model import ImportModel


def list_working_directories() -> list[Path]:
    valid_directories = [
        directory
        for directory in SOURCE_FOLDER.iterdir()
        if directory.name not in FILES_TO_SKIP
    ]
    return valid_directories

def valid_py_files() -> list[Path]:
    py_files: list[Path] = [
        file
        for file_path in list_working_directories()
        for file in file_path.rglob(FILE_EXTENSION)
    ]
    return py_files

def read_py_files() -> list[str]:
    imports: list[str] = []
    for file_path in valid_py_files():
        with file_path.open() as f:
            for line in f:
                if line.startswith('import'):
                    imports.append(line.split(' ')[1].strip())
                elif line.startswith('from'):
                    imports.append(line.split(' ')[1].strip())
    return imports

def import_info() ->  list[ImportModel]:
    imports:  list[ImportModel] = []
    version: str
    description: str
    requires: str
    for imp in read_py_files():
        import_info = subprocess.run(['pip', 'show', imp], capture_output=True, text=True)
        for line in import_info.stdout.splitlines():
            if line.startswith('Version:'):
                version = line.split(':')[1].strip()
            if line.startswith('Requires:'):
                requires = line.split(':')[1].strip()
            if line.startswith('Summary:'):
                description = line.split(':')[1].strip()
        import_model = ImportModel(
            import_name=imp,
            version=version or 'latest',
            description=description or 'No description available',
            requires=requires or 'No requires',
        )
        imports.append(import_model)
    return imports

def write_req_file() -> None:
    req_path = Path(SOURCE_FOLDER/REQ_FILE)
    if os.path.exists(req_path):
        os.remove(req_path)
    req_path.touch()
    for imp in import_info():
        with open(req_path, 'a') as f:
            f.write(
                f"# Description: {imp.description}\n# Requirements: {imp.requires}\n{imp.import_name}=={imp.version}\n"
            )
        f.close()

if __name__ == '__main__':
    write_req_file()