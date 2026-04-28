import std.json;
void main() {
auto my_data = JSONValue([
    // Server configuration
    "host": JSONValue("localhost"),  // default host
    "port": JSONValue(8080),
    // Enable debug mode
    "debug": JSONValue(true),
]);
}
