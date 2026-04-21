import std.json;
void _check() {
int process(T...)(T args) { return 0; }
process(JSONValue([
    JSONValue(1),
]));
}
