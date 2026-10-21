import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto value = JSONValue(1);
process(value);
}
