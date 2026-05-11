import std.json;
void main() {
int process(T...)(T args) { return 0; }
process("hello", "a");
process(42, "b");
process(true, "c");
}
