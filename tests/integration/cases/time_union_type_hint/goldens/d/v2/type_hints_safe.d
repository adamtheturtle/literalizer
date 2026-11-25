import std.json;
void main() {
auto my_data = JSONValue([
    "mixed": JSONValue([JSONValue([JSONValue("09:30:00")]), parseJSON("[]")]),
]);
}
