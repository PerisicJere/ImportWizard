# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from constants import SOURCE_FOLDER, FILE_EXTENSION
import subprocess
from import_model import ImportModel
from flow_compose import flow, flow_function, FlowFunction, FlowArgument


@flow_function(cached=True)
def valid_py_files(target_folder: FlowFunction[str] = None) -> list[Path]:
    folder_to_use = Path(target_folder()) if target_folder else SOURCE_FOLDER
    py_files: list[Path] = [
        file
        for file in folder_to_use.rglob(FILE_EXTENSION)
        ]
    return py_files

@flow_function(cached=True)
def read_py_files(valid_files: FlowFunction[list[Path]]) -> list[str]:
    imports: list[str] = []
    for file_path in valid_files():
        with file_path.open() as f:
            for line in f:
                if line.startswith('import'):
                    imports.append(line.split(' ')[1].strip())
                elif line.startswith('from'):
                    imports.append(line.split(' ')[1].strip())
    return imports

@flow_function(cached=True)
def check_if_import_names_are_correct(read_files: FlowFunction[list[str]]) -> list[str]:
    cleaned_imports: list[str] = []
    for imp in read_files():
        if "." in imp:
            cleaned_imports.append(imp.split(".")[0].strip())
        else:
            cleaned_imports.append(imp)
    return cleaned_imports

@flow_function(cached=True)
def get_import_info(check_import_names: FlowFunction[list[str]]) -> list[ImportModel]:
    imports: list[ImportModel] = []
    version: str
    description: str
    requires: str
    for imp in check_import_names():
        import_info = subprocess.run(['pip', 'show', imp], capture_output=True, text=True)
        if import_info.returncode == 0:
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

@flow_function(cached=True)
def generate_used_imports(import_info: FlowFunction[list[ImportModel]]) -> None:
    for imp in import_info():
        print(f"{imp.import_name}=={imp.version}")

@flow(
    target_folder=FlowArgument(str, default=str(SOURCE_FOLDER)),
    valid_files=valid_py_files,
    read_files=read_py_files,
    check_import_names=check_if_import_names_are_correct,
    import_info=get_import_info,
    generate_imports=generate_used_imports,
)
def main_flow(generate_imports: FlowFunction[None]) -> None:
    generate_imports()
