module Fixture_multiline_string_Crystal_string_format_multiline
extend self
my_data = [
    %q|first line
  indented

last line|,
    %q|
leading newline|,
    " \t\nleading whitespace",
    %q|trailing newline
|,
    %q|
leading and trailing
|,
    %q|quotes: """ ''' ` and backslash: \|,
    %q|interpolation: ${value} #{value} #@value #$value $value|,
    %q|backslash before newline: \
next line|,
    "trailing spaces  \nnext",
    %q|C++ delimiter collision: )LITERALIZER"
value|,
    %q|Rust delimiter collision: "#
value|,
    %q|Lua delimiter collision: ]]
value|,
    "Ruby fallback interpolation  \n\#{expression} #@instance #$global",
    "NUL followed by a digit: \x007",
    "carriage\rreturn",
]
end
