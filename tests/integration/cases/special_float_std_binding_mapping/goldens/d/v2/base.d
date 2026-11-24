import std.json;
void main() {
auto std = JSONValue([
    "nan": JSONValue(double.nan),
    "positive": JSONValue(double.infinity),
    "negative": JSONValue(-double.infinity),
]);
}
