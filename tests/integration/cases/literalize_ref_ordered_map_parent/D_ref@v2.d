import std.json;
void main() {
auto bound = JSONValue(2);
auto my_data = JSONValue([
    JSONValue([JSONValue("value"), bound]),
]);
}
