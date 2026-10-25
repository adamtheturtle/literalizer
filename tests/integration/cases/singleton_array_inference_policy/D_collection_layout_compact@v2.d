import std.json;
void main() {
auto my_data = JSONValue([
    "below": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(1)])])])])])])])]),
    "boundary": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(2)])])])])])])])])]),
    "multiple": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(3)])])])])])])])])])])])])])])])])]),
    "text": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue("value")])])])])])])])])]),
    "boolean": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(true)])])])])])])])])]),
    "float": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(1.5)])])])])])])])])]),
]);
}
