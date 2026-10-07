import std.json;
void main() {
auto integer_value = JSONValue(1.0);
auto my_data = JSONValue([
    integer_value,
    JSONValue(1.5),
]);
}
