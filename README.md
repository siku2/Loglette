# Loglette

[![Build Status](https://travis-ci.org/siku2/Loglette.svg?branch=master)](https://travis-ci.org/siku2/Loglette)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5481332c7e354747983d9233023bdf37)](https://www.codacy.com/app/siku2/Loglette?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=siku2/Loglette&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/siku2/Loglette/branch/master/graph/badge.svg)](https://codecov.io/gh/siku2/Loglette)

> This is an unfinished project and doesn't even have a documentation yet so you might want to leave for now (while you still can) and come back later

A tool for parsing changelogs into all kinds of formats.

## Format
You can read about the Loglette Format Specification (v1) [here][loglette-spec].

## Installing
#### Nice and easy
`pip install loglette`

There are multiple extra dependencies for various reasons.
If you want to have it all you can use `all` (`pip install loglette[all]`)
which installs all possible dependencies.

#### Using Pipenv
Download the repository and use `pipenv install`


## Usage
`loglette [-f FORMAT] file`

`FORMAT` is an alias of a [formatter](loglette-formatters)


[loglette-spec]: http://siku2.github.io/Loglette/spec "Format Specification"
[loglette-formatters]: http://siku2.github.io/Loglette/formatters "Formatters"