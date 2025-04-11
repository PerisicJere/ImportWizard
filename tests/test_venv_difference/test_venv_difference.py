# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest import TestCase
import io
from contextlib import redirect_stdout

from compare_venv_and_imports import venv_flow


class TestVenvDifference(TestCase):
    def test_venv_difference(self):
        with io.StringIO() as stream, redirect_stdout(stream):
            venv_flow(set_function="-d")
            output = stream.getvalue()
        self.assertEqual(output, "")
