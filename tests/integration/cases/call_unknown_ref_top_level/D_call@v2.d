import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto unknown_value = JSONValue([
    JSONValue(1),
]);
process(unknown_value);
}
