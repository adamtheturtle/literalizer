import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto existing = JSONValue(42);
process(existing);
}
