import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_ints = JSONValue([
    JSONValue(1),
    JSONValue(2),
    JSONValue(3),
]);
auto my_strings = JSONValue([
    JSONValue("a"),
    JSONValue("b"),
]);
auto my_empty = parseJSON("[]");
process(my_ints, 42);
process(my_strings, 7);
process(my_empty, 99);
}
