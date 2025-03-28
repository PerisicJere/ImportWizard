# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re
from pathlib import Path
from typing import Final

FILES_TO_SKIP: list[str] = [
    "venv",
    ".idea",
]

SOURCE_FOLDER: Path = (
            Path(__file__).parent.parent
        )

FILE_EXTENSION: str = "*.impwiz"

IMPORT_REGEX: Final = re.compile(
    r"^import (?P<import>[\w.]+)$"
)
FROM_IMPORT_REGEX: Final = re.compile(
    r"from (?P<from>[\w.]+)$"
)

REQ_FILE: Final = "requirements.txt"