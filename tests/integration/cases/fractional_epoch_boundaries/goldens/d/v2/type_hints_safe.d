import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("1970-01-01T00:00:00.000001+00:00"),
    JSONValue("1969-12-31T23:59:59.500000+00:00"),
    JSONValue("1970-01-01T00:00:01+00:00"),
]);
}
