import std.json;
void main() {
auto ref_data = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto my_data = JSONValue([
    JSONValue(0),
]);
(void)my_data;
my_data = ref_data;
(void)my_data;
}
