import std.json;
void main() {
auto array_value = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto scalar_value = JSONValue(3);
auto my_data = JSONValue([
    array_value,
    scalar_value,
]);
}
