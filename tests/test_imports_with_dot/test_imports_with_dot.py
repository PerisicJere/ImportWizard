# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase

from read_impwiz_files import used_imports_flow


class TestExistingImports(TestCase):
    def test_imports_with_dot(self):
        with io.StringIO() as stream, redirect_stdout(stream):
            used_imports_flow(
                target_folder=str(
                    f"{Path(__file__).parent.parent}/test_imports_with_dot"
                )
            )
            output = stream.getvalue()
        self.assertEqual(
            output, "pydantic==2.11.0\npandas==2.2.3\nmatplotlib==3.10.1\n"
        )
