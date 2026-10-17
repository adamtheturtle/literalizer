import std.json;
void main() {
auto my_data = JSONValue([
    "cr": JSONValue("a\rb"),
    "crlf": JSONValue("a\r\nb"),
    "lf": JSONValue("a\nb"),
]);
}
