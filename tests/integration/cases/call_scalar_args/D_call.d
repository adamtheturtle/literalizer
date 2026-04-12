import std.json;
auto process(T...)(T args) { return 0; }
void _check() {
process("hello")
process(42)
process(true)
}
