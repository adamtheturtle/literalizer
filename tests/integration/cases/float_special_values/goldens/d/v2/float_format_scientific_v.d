import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(double.infinity),
    JSONValue(-double.infinity),
    JSONValue(double.nan),
]);
}
