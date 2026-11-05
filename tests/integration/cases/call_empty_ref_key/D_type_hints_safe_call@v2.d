import std.json;
void main() {
int consume(T...)(T args) { return 0; }
auto external_value = JSONValue(1);
consume(external_value);
}
