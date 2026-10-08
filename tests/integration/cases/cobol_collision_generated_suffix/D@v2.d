import std.json;
void main() {
auto my_data = JSONValue([
    "a-b": JSONValue(1),
    "a b": JSONValue(2),
    "a-b-2": JSONValue(3),
]);
}
