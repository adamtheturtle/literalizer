import std.json;
void main() {
auto my_data = JSONValue([
    "single_map": JSONValue([parseJSON("{}")]),
    "single_list": JSONValue([JSONValue([JSONValue(1)])]),
    "single_deep": JSONValue([JSONValue([JSONValue([JSONValue(2)])])]),
]);
}
