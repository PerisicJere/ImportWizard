# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pydantic import BaseModel


class ImportModel(BaseModel):
    import_name: str
    version: str
    description: str
    requires: str
