# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase

from pandas.compat import set_function_name

from compare_poetry_and_imports import poetry_flow


class TestIntersectionPoetry(TestCase):
    def test_intersection_poetry(self):
        with io.StringIO() as stream, redirect_stdout(stream):
            poetry_flow(target_folder=str(f"{Path(__file__).parent.parent}/test_poetry"), set_function="-i")
            output = stream.getvalue()
        self.assertEqual(output, "pydantic==2.11.0\n")