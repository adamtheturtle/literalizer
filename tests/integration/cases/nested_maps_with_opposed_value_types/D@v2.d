import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["input": JSONValue(["name": JSONValue("alice"), "city": JSONValue("paris")]), "expected": JSONValue(["count": JSONValue(1), "total": JSONValue(2)])]),
    JSONValue(["input": JSONValue(["name": JSONValue(10), "city": JSONValue(20)]), "expected": JSONValue(["count": JSONValue("done"), "total": JSONValue("pending")])]),
]);
}
