"""
This is equivalent to the poetry PEP-517 buildsystem API, except before
calling out to poetry it applies our patch to allow the version string
to be set to SCM.
"""
from poetry.core.factory import Factory
from poetry.core.masonry.api import (  # noqa
    build_editable,
    build_sdist,
    build_wheel,
    get_requires_for_build_editable,
    get_requires_for_build_sdist,
    get_requires_for_build_wheel,
    prepare_metadata_for_build_editable,
    prepare_metadata_for_build_wheel,
)

from poetry_scm_version.patch import MonkeyPatchPoetry

MonkeyPatchPoetry.patch(Factory)
