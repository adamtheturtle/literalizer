import std.json;
void main() {
auto my_data = JSONValue([
    "within_i32": JSONValue("2024-01-15T12:00:00"),
    "beyond_i32": JSONValue("2099-06-15T08:30:00"),
]);
}
