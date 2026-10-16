import std.json;
void main() {
auto my_data = JSONValue([
    // heading
    "a": JSONValue("single ' // data"),
    "b": JSONValue("linecontinuation"),
    "c": JSONValue("\\"),  // actual comment
    "d": JSONValue("  "),  // final comment
]);
}
