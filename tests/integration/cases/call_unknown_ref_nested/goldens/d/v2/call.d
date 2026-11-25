import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto known_value = JSONValue(true);
auto unknown_value = JSONValue(true);
process(known_value, unknown_value);
}
