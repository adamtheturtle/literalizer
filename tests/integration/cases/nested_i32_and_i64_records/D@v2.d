import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["value": JSONValue(1)])]),
    JSONValue([JSONValue(["value": JSONValue(1099511627776)])]),
]);
}
