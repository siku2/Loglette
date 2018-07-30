# Loglette

[![Build Status](https://travis-ci.org/siku2/Loglette.svg?branch=master)](https://travis-ci.org/siku2/Loglette)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5481332c7e354747983d9233023bdf37)](https://www.codacy.com/app/siku2/Loglette?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=siku2/Loglette&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/siku2/Loglette/branch/master/graph/badge.svg)](https://codecov.io/gh/siku2/Loglette)

> This is an unfinished project and doesn't even have a proper documentation yet so you might want to leave for now (while you still can) and come back later

A tool for parsing changelogs into all kinds of formats.

### Loglette Format
Loglette isn't *just* a changelog parser, it also aims to be a changelog format.
You can read about the Loglette Format Specification (v1) [here][loglette-spec].
Of course Loglette also parses [other formats][Formatter].

## Installing
#### Nice and easy
`pip install loglette`

There are multiple extra dependencies for various reasons.
If you want to have it all you can use `all` (`pip install loglette[all]`)
which installs all possible dependencies.

#### Using Pipenv
Download the repository and use `pipenv install`


## Usage
`loglette [OPTIONS] file`

#### Options
| short |   long   |              value             |                    description                     |
| ----: | -------- | ------------------------------ | -------------------------------------------------- |
| -f    | --format | *(Optional)* [Formatter] Alias | Use the given [Formatter] to format the changelog.<br>Defaults to [Markdown][Formatter-Markdown]
| -p    | --parser | *(Optional)* [Parser] Alias    | Specify the parser to use when parsing the file.<br>When omitted Loglette tries to guess the correct parser.





[loglette-spec]:        https://siku2.github.io/Loglette/spec "Format Specification"

[Formatter]:            https://siku2.github.io/Loglette/formatters "Formatters"
[Formatter-Markdown]:   https://siku2.github.io/Loglette/formatters#markdown-formatter "Markdown Formatter"
[Parser]:               https://siku2.github.io/Loglette/parsers "Parsers"