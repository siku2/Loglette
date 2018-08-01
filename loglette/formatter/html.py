from textwrap import dedent

from . import formatter
from .special import GroupTypes
from ..changelog import Changelog, ReleaseDate

try:
    from jinja2 import Template
    from mistune import Markdown
except ImportError as e:
    missing = str(getattr(e, "name", "Jinja2 or Mistune"))
    _ERROR = ImportError(f"You don't have {missing} installed. You can use the extra dependency html to automatically install them "
                         f"(pip install loglette[html]) or install them manually (pip install mistune jinja2)")
    _ERROR.__cause__ = e
else:
    _ERROR = None

    HTML_TEMPLATE = Template(dedent("""
    <div class="changelog-header">
        Version <span class="version">{{ changelog.version }}</span>
    </div>
    <div class="changelog-content">
        {% for change_type, changes in change_types.items() -%}
            <div class="changes-category category-{{ change_type|lower }}">
                <div class="category-title">{{ change_type }}</div>
                <div class="category-content">
                    {% for change in changes -%}
                        <div class="change-text priority-{{ change.priority }}">{{ md2html(change.text)|safe }}</div>
                    {% endfor -%}
                </div>
            </div>
        {% endfor -%}
    </div>
    """))

    md_parser = Markdown()


    def md2html(md: str) -> str:
        return md_parser.render(md)


@formatter("html")
class HtmlFormatter(GroupTypes):
    def format(self, changelog: Changelog, **options) -> str:
        if _ERROR:
            raise _ERROR

        change_types = super().format(changelog, **options)

        if isinstance(changelog.release_date, ReleaseDate):
            release = changelog.release_date.value
        else:
            release = changelog.release_date.strftime(options.get("time_format", "%d %b %Y"))

        template = options.get("template", HTML_TEMPLATE)
        if isinstance(template, str):
            template = Template(template)

        return template.render(changelog=changelog, change_types=change_types, release=release, options=options, md2html=md2html)
