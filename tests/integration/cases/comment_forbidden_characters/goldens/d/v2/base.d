import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(1),  // tab	here and bidi <U+202E>after
    "b": JSONValue(2),
]);
}
