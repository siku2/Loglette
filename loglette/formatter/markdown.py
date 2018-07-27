from . import formatter
from .special import GroupTypes
from ..changelog import Changelog


@formatter("markdown", "md")
class MarkdownFormatter(GroupTypes):
    def format(self, changelog: Changelog, **options) -> str:
        change_types = super().format(changelog, **options)

        if changelog.release_date:
            release = changelog.release_date.strftime(options.get("time_format", "%d %b %Y"))
        else:
            release = "Unreleased"

        markdown = [f"# Version {changelog.version} ({release})"]

        for change_type, changes in change_types.items():
            markdown.append(f"\n### {change_type}")
            for change in changes:
                if change.priority:
                    text = f"**{change.text}**"
                else:
                    text = change.text

                markdown.append(f"- {text}")

        return "\n".join(markdown)
