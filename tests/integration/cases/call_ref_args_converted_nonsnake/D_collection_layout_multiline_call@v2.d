import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_var = JSONValue([
    JSONValue(1),
    JSONValue(2),
    JSONValue(3),
]);
auto my_other = JSONValue([
    JSONValue(4),
    JSONValue(5),
    JSONValue(6),
]);
process(my_var, 42);
process(my_other, 7);
}
