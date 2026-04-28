import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1.500000), JSONValue(2.500000)]),
    JSONValue([JSONValue(3.500000), JSONValue(4.500000)]),
]);
}
