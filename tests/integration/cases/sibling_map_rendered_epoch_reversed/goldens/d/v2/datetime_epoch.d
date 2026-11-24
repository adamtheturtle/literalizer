import std.json;
void main() {
auto my_data = JSONValue([
    "b": JSONValue(["k": JSONValue(1)]),
    "a": JSONValue(["k": JSONValue(2208988800)]),
]);
}
