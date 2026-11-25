import std.json;
void main() {
auto deep = JSONValue([
    JSONValue([
        JSONValue("one"),
        JSONValue("two"),
    ]),
    JSONValue([
        JSONValue("three"),
        JSONValue("four"),
    ]),
]);
auto my_data = JSONValue([
    "a": JSONValue([
        "b": JSONValue([
            "c": deep,
        ]),
    ]),
]);
}
