import std.json;
void main() {
auto my_data = JSONValue([
    "double": JSONValue("a b"),
    "single": JSONValue("c d"),
    // A comment, which both separators would end.
    "both": JSONValue("e f g"),
    "continued": JSONValue("hi"),
    "escaped backslash": JSONValue("j\\ k"),
]);
}
