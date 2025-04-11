# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from unittest import TestCase
import io
from contextlib import redirect_stdout

from compare_venv_and_imports import venv_flow


class TestVenv(TestCase):
    def test_venv(self):
        with io.StringIO() as stream, redirect_stdout(stream):
            venv_flow()
            output = stream.getvalue()
        self.assertEqual(
            output,
            """annotated-types==0.7.0
contourpy==1.3.1
cycler==0.12.1
flow-compose==0.3.9
fonttools==4.56.0
kiwisolver==1.4.8
makefun==1.15.6
matplotlib==3.10.1
numpy==2.2.4
packaging==24.2
pandas==2.2.3
pillow==11.1.0
pip==25.0.1
pydantic==2.11.0
pydantic_core==2.33.0
pyparsing==3.2.3
python-dateutil==2.9.0.post0
pytz==2025.2
ruff==0.11.5
six==1.17.0
tomlkit==0.13.2
tzdata==2025.2
""",
        )
