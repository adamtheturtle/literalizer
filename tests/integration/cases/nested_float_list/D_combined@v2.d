import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1.5), JSONValue(2.5)]),
    JSONValue([JSONValue(3.5), JSONValue(4.5)]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(1.5), JSONValue(2.5)]),
    JSONValue([JSONValue(3.5), JSONValue(4.5)]),
]);
}
