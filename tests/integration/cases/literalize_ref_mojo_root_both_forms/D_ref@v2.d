import std.json;
void main() {
auto whole = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto my_data = whole;
my_data = whole;
}
