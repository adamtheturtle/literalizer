import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(""), JSONValue("unnamed")]),
    JSONValue([JSONValue("named"), JSONValue("value")]),
]);
}
