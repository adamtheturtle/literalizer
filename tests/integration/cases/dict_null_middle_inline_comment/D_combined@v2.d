import std.json;
void main() {
auto my_data = JSONValue([
    "host": JSONValue("localhost"),
    "port": JSONValue(null),  // not configured yet
    "debug": JSONValue(true),
]);
my_data = JSONValue([
    "host": JSONValue("localhost"),
    "port": JSONValue(null),  // not configured yet
    "debug": JSONValue(true),
]);
}
