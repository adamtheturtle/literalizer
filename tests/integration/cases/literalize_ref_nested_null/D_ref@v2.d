import std.json;
void main() {
auto my_null = JSONValue(null);
auto my_data = JSONValue([
    my_null,
    JSONValue(null),
]);
}
