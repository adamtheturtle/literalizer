import std.json;
void main() {
auto my_data = JSONValue([
    "scores": JSONValue([JSONValue(10), JSONValue(20), JSONValue(30)]),
    "args": JSONValue([JSONValue(1), JSONValue("email"), JSONValue("a@gmail.com"), JSONValue(100)]),
]);
my_data = JSONValue([
    "scores": JSONValue([JSONValue(10), JSONValue(20), JSONValue(30)]),
    "args": JSONValue([JSONValue(1), JSONValue("email"), JSONValue("a@gmail.com"), JSONValue(100)]),
]);
}
