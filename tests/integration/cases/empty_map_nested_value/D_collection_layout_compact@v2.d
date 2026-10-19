import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["mapping": parseJSON("{}")]), parseJSON("{}")]),
    JSONValue([parseJSON("{}"), JSONValue(["mapping": parseJSON("{}")])]),
]);
}
