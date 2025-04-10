# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase

from compare_poetry_and_imports import poetry_flow


class TestPoetry(TestCase):
    def test_poetry(self):
        with io.StringIO() as stream, redirect_stdout(stream):
            poetry_flow(target_folder=str(f"{Path(__file__).parent.parent}/test_poetry"))
            output = stream.getvalue()
        self.assertEqual(output, "MarkupSafe>=2.0\nannotated-types>=0.6.0\ncfgv>=2.0.0\ndistlib>=0.3.7,<1\nfilelock>=3.12.2,<4\nidentify>=1.0.0\njinja2==3.1.5\nmarkupsafe==3.0.2\nmypy-extensions==1.0.0\nmypy==1.11.1\nnodeenv>=0.11.1\nplatformdirs>=3.9.1,<5\npre-commit==3.8.0\npydantic-core==2.27.2\npyyaml==6.0.2\nruff==0.6.4\ntomli==2.2.1\ntyping-extensions==4.12.2\nvirtualenv==20.29.2\n")