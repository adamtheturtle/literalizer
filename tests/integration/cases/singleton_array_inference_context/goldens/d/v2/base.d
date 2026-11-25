import std.json;
void main() {
auto my_data = JSONValue([
    "nil": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(null)])])])])])])])])]),
    "empty": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([parseJSON("[]")])])])])])])])])]),
    "siblings": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(4), JSONValue(5)])])])])])])])])])]),
]);
}
