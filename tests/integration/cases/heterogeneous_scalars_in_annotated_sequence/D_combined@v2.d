import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(true),
    JSONValue(1.5),
    JSONValue(null),
    JSONValue("2020-01-01"),
    JSONValue("2020-01-01T00:00:00+00:00"),
    parseJSON("[]"),
]);
my_data = JSONValue([
    JSONValue(true),
    JSONValue(1.5),
    JSONValue(null),
    JSONValue("2020-01-01"),
    JSONValue("2020-01-01T00:00:00+00:00"),
    parseJSON("[]"),
]);
}
