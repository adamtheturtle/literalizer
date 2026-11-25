import std.json;
void main() {
auto my_data = JSONValue([
    "outer": JSONValue([JSONValue([JSONValue("nested first line\n  indented\n\nnested last line\n")])]),
]);
}
