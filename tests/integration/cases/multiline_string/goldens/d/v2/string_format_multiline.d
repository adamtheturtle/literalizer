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
    JSONValue(`C++ empty delimiter collision: )"
value`),
    JSONValue(`C++ first fallback collision: )" and )x"
value`),
    JSONValue(`C++ second fallback collision: )" and )x" and )x0"
value`),
    JSONValue(`Rust delimiter collision: "#
value`),
    JSONValue(`Lua delimiter collision: ]]
value`),
    JSONValue(`Swift delimiter collision: """#
value`),
    JSONValue(`Swift interpolation collision: \#(value)
value`),
    JSONValue("Ruby fallback interpolation  \n#{expression} #@instance #$global"),
    JSONValue("NUL followed by a digit: \x007"),
    JSONValue("carriage\rreturn"),
]);
}
