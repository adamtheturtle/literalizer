import std.json;
void main() {
auto my_data = JSONValue([
    // Configuration
    "name": JSONValue("app"),
    // Port setting
    "port": JSONValue(3000),
]);
}
