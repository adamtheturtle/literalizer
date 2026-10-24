import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["scores": JSONValue([JSONValue(1), JSONValue(2)])]),
    JSONValue(["scores": JSONValue([JSONValue(3), JSONValue(4)])]),
]);
}
