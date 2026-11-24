import std.json;
void main() {
auto my_data = JSONValue([
    "name": JSONValue("Alice"),
    "age": JSONValue(30),
    "active": JSONValue(true),
    "score": JSONValue(null),
    "joined": JSONValue("2024-01-15"),
    "last_login": JSONValue("2024-01-15T12:30:00+00:00"),
    "avatar": JSONValue("48656c6c6f"),
]);
}
