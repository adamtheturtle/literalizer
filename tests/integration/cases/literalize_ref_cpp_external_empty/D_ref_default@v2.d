import std.json;
void main() {
auto item = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto my_data = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
(void)my_data;
my_data = item;
(void)my_data;
}
