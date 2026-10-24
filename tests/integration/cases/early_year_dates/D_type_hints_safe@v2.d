import std.json;
void main() {
auto my_data = JSONValue([
    "date": JSONValue("0099-05-27"),
    "naive": JSONValue("0001-01-01T12:30:00"),
    "recent": JSONValue("2024-05-27T10:00:00"),
]);
}
