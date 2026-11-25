import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_int = JSONValue(1);
auto my_bool = JSONValue(true);
auto my_float = JSONValue(3.14);
auto my_list = JSONValue([
    JSONValue(1),
    JSONValue(2),
    JSONValue(3),
]);
process(my_int, 42);
process(my_bool, 7);
process(my_float, 9);
process(my_list, 1);
}
