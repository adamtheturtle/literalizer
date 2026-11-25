import std.json;
void main() {
auto my_data = JSONValue([
    "explicit_string": JSONValue("5"),
    "six": JSONValue("explicitly tagged key"),
]);
}
