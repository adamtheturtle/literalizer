import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("first line\n  indented\n\nlast line"),
    JSONValue("\nleading newline"),
    JSONValue(" \t\nleading whitespace"),
    JSONValue("trailing newline\n"),
    JSONValue("\nleading and trailing\n"),
    JSONValue("quotes: \"\"\" ''' ` and backslash: \\"),
    JSONValue("interpolation: ${value} #{value} #@value #$value $value"),
    JSONValue("backslash before newline: \\\nnext line"),
    JSONValue("trailing spaces  \nnext"),
    JSONValue("C++ empty delimiter collision: )\"\nvalue"),
    JSONValue("C++ first fallback collision: )\" and )x\"\nvalue"),
    JSONValue("C++ second fallback collision: )\" and )x\" and )x0\"\nvalue"),
    JSONValue("Rust delimiter collision: \"#\nvalue"),
    JSONValue("Lua delimiter collision: ]]\nvalue"),
    JSONValue("Swift delimiter collision: \"\"\"#\nvalue"),
    JSONValue("Swift interpolation collision: \\#(value)\nvalue"),
    JSONValue("Ruby fallback interpolation  \n#{expression} #@instance #$global"),
    JSONValue("NUL followed by a digit: \x007"),
    JSONValue("carriage\rreturn"),
]);
}
