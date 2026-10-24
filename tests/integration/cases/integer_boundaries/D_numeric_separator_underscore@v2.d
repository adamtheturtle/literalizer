import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(long.min),
    JSONValue(9_223_372_036_854_775_808UL),
]);
}
