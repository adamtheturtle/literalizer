import std.json;
void main() {
auto my_data = JSONValue([
    "host": JSONValue("it's here"),  // a comment
    "port": JSONValue(80),  // another
]);
my_data = JSONValue([
    "host": JSONValue("it's here"),  // a comment
    "port": JSONValue(80),  // another
]);
}
