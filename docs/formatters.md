# Formatters
This is a list of all the supported formatters for Loglette.
You can specify the formatter to use by using the `-f <formatter>` argument
where `<formatter>` is an alias of the formatter you want to use.

Example: `-f md` and `-f markdown` select the Markdown Formatter 
(which is the default anyway)

### General Options:
`time_format` (optional): [strftime format template][strftime-behaviour] for the release date




## Markdown Formatter
Aliases: `md`, `markdown`

#### Options
This formatter currently doesn't support any options (apart from the general options)




## HTML Formatter
Aliases: `html`

> The HTML Formatter requires [Mistune][mistune-homepage] and [Jinja2][jinja2-homepage]
to be installed! You can make use of the extra dependency `html`
to automatically install them:<br>
`pip install loglette[html]`

#### Options
`template` (optional): A [Jinja2 template string][jinja2-templates].
The template is rendered using the following variables:

|   Variable    | Description
| ------------- | ----------------------------------------------------
| changelog     | The [Changelog] instance being formatted
| change_types  | A dictionary mapping the name of a change_type to a list of all the changes the belong to it
| release       | The formatted release date
| options       | Options passed to the formatter
| **md2html**   | A function that converts a markdown string to HTML




[strftime-behaviour]: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior "Python Documentation on time formatting"

[mistune-homepage]: https://github.com/lepture/mistune "Mistune Homepage"

[jinja2-homepage]: http://jinja.pocoo.org/ "Jinja2 Homepage"
[jinja2-templates]: http://jinja.pocoo.org/docs/2.10/templates/ "Jinja2 Templates Documentation"