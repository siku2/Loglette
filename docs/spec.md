# Format specification v1

## File format:
```
version: <version>;
release: <release_date>;
---
<logs>
```

Multiple changelogs are separated using `===`.

### Example:
```
version: 1.0.0;
release: 2018;
---
added: Every feature there is;

===

version: 0.0.1;
release: 2017;
---
added: All of the bugs;
```

Loglette uses semicolons to terminate statements in order to make multi-line statements easy.
Don't forget to add a semicolon after each "line" otherwise you'll get interesting results.


## Log format:
```yaml
<type><[<priority>] (optional)>: <text style (YAML)> <text>;
```

#### \<type\>
Following the [guidelines from Keep a Changelog][keepachangelog-how]
`<type>` should be any of: <br>
`added`
`changed`
`deprecated`
`removed`
`fixed`
`security`

This however isn't enforced.
Internally `<type>` is converted to uppercase and the output casing
depends on the [`Formatter`].

#### \<priority\>
`<priority>` is an **optional** non-negative integer which defaults to 0.
The effect on the output strongly depends on the [`Formatter`].

#### \<text style\>
You may provide a style hint for the log text based on the [YAML][yaml-home] thingy thing (TODO).



## Examples
```yaml
added: A changelog parser to parse this file;
```
```yaml
CHANGED[2]: >
            The type will be capitalised internally
            and your text can span over multiple lines!
            It will even get dedented;
```
```yaml
DEPRECATED: |
If you want to have your text all over the place (I mean, why not?)
            you can use the pipe character;
```
```yaml
	security: Feel free to indent your things btw, doesn't really matter;
```
```yaml
// Comments are also a thing
Actually, everything is a comment as long as it doesn't match the format above so knock yourself out
   mind_you_comma_if: you write like this, it will be detected if you don't add the //;
//quack: this won't break a thing;
```



[`Formatter`]: #formatter

[keepachangelog-how]:   https://keepachangelog.com/en/1.0.0/#how    "Keep a Changelog Change Types"
[yaml-home]:            http://yaml.org/    "Official YAML Web Site"