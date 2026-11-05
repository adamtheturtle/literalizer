import std.json;
void main() {
auto ref_data = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto my_data = ref_data;
}
