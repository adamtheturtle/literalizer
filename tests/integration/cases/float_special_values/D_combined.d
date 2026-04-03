import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue(double.infinity),
    JSONValue(-double.infinity),
    JSONValue(double.nan),
]);
my_data = JSONValue([
    JSONValue(double.infinity),
    JSONValue(-double.infinity),
    JSONValue(double.nan),
]);
}
