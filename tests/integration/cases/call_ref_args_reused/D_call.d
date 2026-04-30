import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto repeated_var = JSONValue(1);
auto single_var = JSONValue([
    JSONValue(4),
    JSONValue(5),
    JSONValue(6),
]);
process(repeated_var, 1);
process(single_var, 0);
process(repeated_var, 8);
}
