import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(`first line
  indented

last line`),
    JSONValue(`
leading newline`),
    JSONValue(" \t\nleading whitespace"),
    JSONValue(`trailing newline
`),
    JSONValue(`
leading and trailing
`),
    JSONValue("quotes: \"\"\" ''' ` and backslash: \\"),
    JSONValue(`interpolation: ${value} #{value} #@value #$value $value`),
    JSONValue(`backslash before newline: \
next line`),
    JSONValue("trailing spaces  \nnext"),
    JSONValue(`C++ delimiter collision: )LITERALIZER"
value`),
    JSONValue(`Rust delimiter collision: "#
value`),
    JSONValue(`Lua delimiter collision: ]]
value`),
    JSONValue("Ruby fallback interpolation  \n#{expression} #@instance #$global"),
    JSONValue("NUL followed by a digit: \x007"),
    JSONValue("carriage\rreturn"),
]);
}
