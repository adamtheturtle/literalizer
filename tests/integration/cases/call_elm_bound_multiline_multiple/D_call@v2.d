import std.json;
void main() {
int f(T...)(T args) { return 0; }
auto ref_data = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
f(JSONValue([
    ref_data,
]));
f(JSONValue([
    ref_data,
]));
}
