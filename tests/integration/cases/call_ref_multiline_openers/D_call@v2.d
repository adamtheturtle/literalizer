import std.json;
void main() {
int consume(T...)(T args) { return 0; }
auto foo = JSONValue(42);
consume(JSONValue([
    JSONValue([
        "other": JSONValue(1),
    ]),
    foo,
]), JSONValue([
    "left": foo,
    "other": JSONValue(1),
]));
}
