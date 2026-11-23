import std.json;
void main() {
auto shared_values = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto my_data = JSONValue([
    "a": shared_values,
]);
my_data = JSONValue([
    "a": shared_values,
]);
}
