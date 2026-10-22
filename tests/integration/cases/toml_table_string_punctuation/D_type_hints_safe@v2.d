import std.json;
void main() {
auto my_data = JSONValue([
    "comma_hash": JSONValue("a,#b"),
    "comma_space_hash": JSONValue("trail, # comment"),
    "escaped_quote": JSONValue("quote \" and , #"),
    "next_line": JSONValue("xy"),
    "line_separator": JSONValue("x y"),
    "paragraph_separator": JSONValue("x y"),
]);
}
