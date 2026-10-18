import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(1),  // inline ending backslash \ .
    "b": JSONValue(2),
]);
}
