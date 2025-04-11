# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


def difference_of_used_imports_and_dependencies(
    dependencies_set: set[str], used_imports: set[str]
) -> None:
    used_imports: set[str] = used_imports
    dependencies: set[str] = dependencies_set
    difference = list(dependencies.difference(used_imports))
    for dif in sorted(difference):
        print(dif)


def intersection_of_used_imports_and_dependencies(
    dependencies_set: set[str], used_imports: set[str]
) -> None:
    used_imports: set[str] = used_imports
    dependencies: set[str] = dependencies_set
    intersection = list(dependencies.intersection(used_imports))
    for inter in sorted(intersection):
        print(inter)
