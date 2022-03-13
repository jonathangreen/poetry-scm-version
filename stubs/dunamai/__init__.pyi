# These stubs are only needed until
# This PR is merged: https://github.com/mtkennerly/dunamai/pull/44
# It works around the library missing Optional[] on some types

import datetime as dt
from enum import Enum
from typing import (
    Any,
    Callable,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

_VERSION_PATTERN: str

class Style(Enum):
    Pep440: str
    SemVer: str
    Pvp: str

class Vcs(Enum):
    Any: str
    Git: str
    Mercurial: str
    Darcs: str
    Subversion: str
    Bazaar: str
    Fossil: str

class _GitRefInfo:
    fullref: Any
    commit: Any
    creatordate: Any
    committerdate: Any
    taggerdate: Any
    tag_topo_lookup: Any
    def __init__(
        self,
        ref: str,
        commit: str,
        creatordate: str,
        committerdate: str,
        taggerdate: str,
    ) -> None: ...
    def with_tag_topo_lookup(self, lookup: Mapping[str, int]) -> _GitRefInfo: ...
    @staticmethod
    def normalize_git_dt(timestamp: str) -> Optional[dt.datetime]: ...
    def best_date(self) -> Optional[dt.datetime]: ...
    @property
    def commit_offset(self) -> int: ...
    @property
    def sort_key(self) -> Tuple[int, Optional[dt.datetime]]: ...
    @property
    def ref(self) -> str: ...
    @staticmethod
    def normalize_tag_ref(ref: str) -> str: ...
    @staticmethod
    def from_git_tag_topo_order() -> Mapping[str, int]: ...

class Version:
    base: Any
    stage: Any
    revision: Any
    distance: Any
    commit: Any
    dirty: Any
    tagged_metadata: Any
    epoch: Any
    branch: Any
    timestamp: Any
    def __init__(
        self,
        base: str,
        *,
        stage: Tuple[str, Optional[int]] = ...,
        distance: int = ...,
        commit: str = ...,
        dirty: bool = ...,
        tagged_metadata: Optional[str] = ...,
        epoch: int = ...,
        branch: str = ...,
        timestamp: dt.datetime = ...
    ) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __lt__(self, other: Any) -> bool: ...
    def serialize(
        self,
        metadata: Optional[bool] = ...,
        dirty: bool = ...,
        format: Union[str, Callable[[Version], str], None] = ...,
        style: Optional[Style] = ...,
        bump: bool = ...,
        tagged_metadata: bool = ...,
    ) -> str: ...
    @classmethod
    def parse(cls, version: str, pattern: str = ...) -> Version: ...
    def bump(self, index: int = ...) -> Version: ...
    @classmethod
    def from_git(cls, pattern: str = ..., latest_tag: bool = ...) -> Version: ...
    @classmethod
    def from_mercurial(cls, pattern: str = ..., latest_tag: bool = ...) -> Version: ...
    @classmethod
    def from_darcs(cls, pattern: str = ..., latest_tag: bool = ...) -> Version: ...
    @classmethod
    def from_subversion(
        cls, pattern: str = ..., latest_tag: bool = ..., tag_dir: str = ...
    ) -> Version: ...
    @classmethod
    def from_bazaar(cls, pattern: str = ..., latest_tag: bool = ...) -> Version: ...
    @classmethod
    def from_fossil(cls, pattern: str = ..., latest_tag: bool = ...) -> Version: ...
    @classmethod
    def from_any_vcs(
        cls, pattern: str = ..., latest_tag: bool = ..., tag_dir: str = ...
    ) -> Version: ...
    @classmethod
    def from_vcs(
        cls, vcs: Vcs, pattern: str = ..., latest_tag: bool = ..., tag_dir: str = ...
    ) -> Version: ...
    def __gt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

def check_version(version: str, style: Style = ...) -> None: ...
def get_version(
    name: str,
    first_choice: Callable[[], Optional[Version]] = ...,
    third_choice: Callable[[], Optional[Version]] = ...,
    fallback: Version = ...,
    ignore: Sequence[Version] = ...,
    parser: Callable[[str], Version] = ...,
) -> Version: ...
def serialize_pep440(
    base: str,
    stage: str = ...,
    revision: int = ...,
    post: int = ...,
    dev: int = ...,
    epoch: int = ...,
    metadata: Sequence[Union[str, int]] = ...,
) -> str: ...
def serialize_semver(
    base: str,
    pre: Sequence[Union[str, int]] = ...,
    metadata: Sequence[Union[str, int]] = ...,
) -> str: ...
def serialize_pvp(base: str, metadata: Sequence[Union[str, int]] = ...) -> str: ...
def bump_version(base: str, index: int = ...) -> str: ...
