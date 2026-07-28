import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto known_value = JSONValue(1);
auto unknown_value = parseJSON("[]");
process(unknown_value);
}
