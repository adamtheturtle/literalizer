import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(-2147483649),
    JSONValue(-2147483648),
    JSONValue(2147483647),
    JSONValue(2147483648),
]);
}
