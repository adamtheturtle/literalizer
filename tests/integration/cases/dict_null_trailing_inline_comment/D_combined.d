import std.json;
void _check() {
auto my_data = JSONValue([
    "host": JSONValue("localhost"),
    "port": JSONValue(null),  // not configured yet
]);
my_data = JSONValue([
    "host": JSONValue("localhost"),
    "port": JSONValue(null),  // not configured yet
]);
}
