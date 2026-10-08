import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["first": JSONValue(1)]),
    JSONValue(["repeated": JSONValue("a")]),
    JSONValue(["repeated": JSONValue("b")]),
]);
}
