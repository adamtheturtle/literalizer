import std.json;
void main() {
auto empty_values = parseJSON("[]");
auto integer_values = JSONValue([
    JSONValue(1),
]);
auto my_data = JSONValue([
    empty_values,
    integer_values,
]);
}
