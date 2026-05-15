import std.json;
void main() {
auto my_data = JSONValue([
    "call": JSONValue("send"),
    "args": JSONValue([JSONValue(1), JSONValue("email"), JSONValue("a@gmail.com"), JSONValue(100)]),
]);
}
