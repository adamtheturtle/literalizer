import std.json;
void main() {
auto deep = JSONValue([
    JSONValue([
        JSONValue(1),
        JSONValue(2),
    ]),
    JSONValue([
        JSONValue(3),
        JSONValue(4),
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
