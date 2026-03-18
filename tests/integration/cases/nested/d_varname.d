import std.json;

void _check() {
auto my_data = JSONValue([
    "users": JSONValue([JSONValue(["name": JSONValue("Bob"), "tags": JSONValue([JSONValue("admin"), JSONValue("user")])]), JSONValue(["name": JSONValue("Carol"), "tags": JSONValue([JSONValue("guest")])])]),
]);
}
