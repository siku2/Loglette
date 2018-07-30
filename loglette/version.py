from itertools import zip_longest
from typing import Iterator, Tuple, Union

VersionCompType = Union["Version", Tuple[int, ...]]


class Version:
    parts: Tuple[int, ...]
    tag: str
    length: int

    def __init__(self, *parts: int, tag: str = None):
        self.parts = tuple(parts)
        self.length = len(self.parts)
        self.tag = tag

    def __repr__(self) -> str:
        ver = ".".join(map(str, self.parts))
        if self.tag:
            ver += f"-{self.tag}"
        return ver

    def __len__(self) -> int:
        return self.length

    def __hash__(self) -> int:
        h = hash(self.parts)
        if self.tag:
            h += hash(self.tag)
        return h

    def __getitem__(self, item: int) -> int:
        return self.parts[item]

    def __iter__(self) -> Iterator[int]:
        return iter(self.parts)

    def __eq__(self, other: VersionCompType) -> bool:
        if not isinstance(other, (Version, tuple)):
            return NotImplemented

        if isinstance(other, Version):
            if not self.same_tag_as(other):
                return False
        return self.same_version_as(other)

    def __gt__(self, other: VersionCompType) -> bool:
        if isinstance(other, (Version, tuple)):
            for self_part, other_part in zip_longest(self, other, fillvalue=0):
                if self_part > other_part:
                    return True
            return False
        return NotImplemented

    def __ge__(self, other: VersionCompType) -> bool:
        if not isinstance(other, (Version, tuple)):
            return NotImplemented
        return self > other or self.same_version_as(other)

    def __lt__(self, other: VersionCompType) -> bool:
        if not isinstance(other, (Version, tuple)):
            return NotImplemented
        for self_part, other_part in zip_longest(self, other, fillvalue=0):
            if self_part < other_part:
                return True
        return False

    def __le__(self, other: VersionCompType) -> bool:
        if not isinstance(other, (Version, tuple)):
            return NotImplemented
        return self < other or self.same_version_as(other)

    @property
    def major(self) -> int:
        if self.length <= 0:
            raise TypeError(f"{self} doesn't have a major part")
        return self.parts[0]

    @property
    def minor(self) -> int:
        if self.length <= 1:
            raise TypeError(f"{self} doesn't have a minor part")
        return self.parts[1]

    @property
    def patch(self) -> int:
        if self.length <= 2:
            raise TypeError(f"{self} doesn't have a patch part")
        return self.parts[2]

    @property
    def is_semantic(self) -> bool:
        return self.length == 3

    @classmethod
    def _from_version_code(cls, v: int, padding=3) -> "Version":
        parts = []
        version_code = str(v)
        for i in range(len(version_code), -1, -padding):
            start = max(i - 3, 0)
            part = version_code[start:i]
            if part:
                parts.insert(0, int(part))
        return cls(*parts)

    @classmethod
    def parse(cls, v: Union[str, int], **kwargs) -> "Version":
        if isinstance(v, int):
            return cls._from_version_code(v, **kwargs)

        elements = v.split("-", maxsplit=1)
        if len(elements) == 2:
            version, tag = elements
            tag = tag.strip()
        else:
            version = elements[0]
            tag = None

        _parts = version.split(".")
        if not all(part.isnumeric() for part in _parts):
            return SpecialVersion(v)

        parts = map(int, _parts)

        return cls(*parts, tag=tag)

    def same_version_as(self, other: VersionCompType) -> bool:
        for self_part, other_part in zip_longest(self, other, fillvalue=0):
            if self_part != other_part:
                return False
        return True

    def same_tag_as(self, other: "Version") -> bool:
        return self.tag == other.tag

    def version_code(self, padding=3) -> int:
        code = ""
        for part in self:
            _part = str(part).rjust(padding, "0")
            if len(_part) > padding:
                raise ValueError(f"{self} has a part ({part}) that is too big to be converted into a version code with padding {padding}")
            code += _part
        if not code:
            return 0
        return int(code)


class SpecialVersion(Version):
    name: str

    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: VersionCompType) -> bool:
        if not isinstance(other, SpecialVersion):
            return NotImplemented
        return self.name == other.name
