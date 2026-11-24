import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("entries"), JSONValue([JSONValue(["id": JSONValue(1)])])]),
]);
}
