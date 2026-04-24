import std.json;
void _check() {
int process(T...)(T args) { return 0; }
auto items = JSONValue([
    process(1, 42),
    process(2, 100),
]);
}
