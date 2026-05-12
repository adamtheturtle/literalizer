import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([
        JSONValue([JSONValue("a"), JSONValue(1)]),
    ]),
    JSONValue("hello"),
]);
}
