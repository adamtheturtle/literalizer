import std.json;
void main() {
auto floating_value = JSONValue(1.5);
auto integer_value = JSONValue(2.0);
auto my_data = JSONValue([
    floating_value,
    integer_value,
]);
}
