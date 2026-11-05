import std.json;
void main() {
int consume(T...)(T args) { return 0; }
auto value = JSONValue(null);
consume(value);
}
