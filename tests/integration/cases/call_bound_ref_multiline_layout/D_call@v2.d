import std.json;
void main() {
int f(T...)(T args) { return 0; }
auto x = JSONValue([
    JSONValue([
        JSONValue(1),
        JSONValue(2),
    ]),
    JSONValue([
        JSONValue(3),
        JSONValue(4),
    ]),
]);
f(JSONValue([
    JSONValue([
        x,
    ]),
]));
}
