import std.json;
void main() {
auto my_data = JSONValue([
    "key": JSONValue("value \" # not a comment"),  // real
]);
my_data = JSONValue([
    "key": JSONValue("value \" # not a comment"),  // real
]);
}
