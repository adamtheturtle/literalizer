import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("ADD"), JSONValue("alice"), JSONValue("hello")]),
    JSONValue([JSONValue("DEL"), JSONValue("bob"), JSONValue("5")]),  // removes "world"
]);
}
