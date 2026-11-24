import std.json;
void main() {
auto empty_values = parseJSON("[]");
auto integer_values = JSONValue([
    JSONValue(1),
]);
auto float_values = JSONValue([
    JSONValue(1.5),
]);
auto my_data = JSONValue([
    empty_values,
    integer_values,
    float_values,
]);
}
