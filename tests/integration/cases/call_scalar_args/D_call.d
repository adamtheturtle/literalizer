import std.json;
void _check() {
auto process(T...)(T args) { return 0; }
process("hello")
process(42)
process(true)
}
