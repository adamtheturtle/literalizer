import std.json;
void main() {
int consume(T...)(T args) { return 0; }
auto my_null = JSONValue(null);
auto regular_null = JSONValue(null);
consume(my_null);
consume(regular_null);
}
