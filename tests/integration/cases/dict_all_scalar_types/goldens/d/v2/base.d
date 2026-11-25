import std.json;
void main() {
auto my_data = JSONValue([
    "s": JSONValue("string"),
    "i": JSONValue(1),
    "f": JSONValue(1.5),
    "b": JSONValue(true),
    "n": JSONValue(null),
    "d": JSONValue("2024-01-15"),
    "dt": JSONValue("2024-01-15T12:00:00"),
    "by": JSONValue("48656c6c6f"),
]);
}
