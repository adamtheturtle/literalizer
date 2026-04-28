import std.json;
void main() {
auto my_data = JSONValue([
    "1": JSONValue("one"),
    "2": JSONValue("two"),
    "42": JSONValue("answer"),
]);
my_data = JSONValue([
    "1": JSONValue("one"),
    "2": JSONValue("two"),
    "42": JSONValue("answer"),
]);
}
