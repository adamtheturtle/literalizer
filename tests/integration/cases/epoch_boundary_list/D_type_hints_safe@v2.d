import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("1901-12-13T20:45:51"),
    JSONValue("1901-12-13T20:45:52"),
    JSONValue("2038-01-19T03:14:07"),
    JSONValue("2038-01-19T03:14:08"),
]);
}
