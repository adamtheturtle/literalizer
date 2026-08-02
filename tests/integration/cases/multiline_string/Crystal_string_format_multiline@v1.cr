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
    %q|C++ empty delimiter collision: )"
value|,
    %q|C++ first fallback collision: )" and )x"
value|,
    %q|C++ second fallback collision: )" and )x" and )x0"
value|,
    %q|Rust delimiter collision: "#
value|,
    %q|Lua delimiter collision: ]]
value|,
    %q|Swift delimiter collision: """#
value|,
    %q|Swift interpolation collision: \#(value)
value|,
    "Ruby fallback interpolation  \n\#{expression} #@instance #$global",
    "NUL followed by a digit: \x007",
    "carriage\rreturn",
]
end
