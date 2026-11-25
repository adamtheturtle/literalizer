import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["outer": JSONValue(["inner": JSONValue(["x": JSONValue(1)])])]),
    JSONValue(["outer": JSONValue(["inner": parseJSON("{}")])]),
]);
}
