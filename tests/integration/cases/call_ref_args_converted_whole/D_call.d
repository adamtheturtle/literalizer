import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_var = JSONValue([
    JSONValue(1),
    JSONValue(2),
    JSONValue(3),
]);
process(my_var);
}
