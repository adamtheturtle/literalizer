import std.json;
void main() {
auto my_data = JSONValue([
    "alpha": JSONValue([JSONValue(2), parseJSON("[]")]),
    "beta": JSONValue([JSONValue(5), JSONValue([JSONValue("x")])]),
]);
}
