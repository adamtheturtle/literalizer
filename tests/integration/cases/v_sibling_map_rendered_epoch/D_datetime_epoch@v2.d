import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["k": JSONValue(2208988800)]),
    "b": JSONValue(["k": JSONValue(1)]),
]);
}
