from collections import defaultdict
from operator import attrgetter
from typing import Dict, List

from . import Formatter
from ..changelog import Change, Changelog


class GroupTypes(Formatter):
    @classmethod
    def group_by_type(cls, changelog: Changelog, sort_priority=True) -> Dict[str, List[Change]]:
        change_types = defaultdict(list)
        for change in changelog.changes:
            change_types[change.change_type].insert(0, change)

        if sort_priority:
            for changes in change_types.values():
                changes.sort(key=attrgetter("priority"), reverse=True)

        return dict(change_types)

    def format(self, changelog: Changelog, **options) -> Dict[str, List[Change]]:
        return self.group_by_type(changelog)
