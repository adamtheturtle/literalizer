import std.json;
void main() {
auto my_data = JSONValue([
    "positive": JSONValue([JSONValue(["item": JSONValue([JSONValue(2147483648)])])]),
    "negative": JSONValue([JSONValue(["item": JSONValue([JSONValue(-2147483649)])])]),
    "mixed": JSONValue([JSONValue(["item": JSONValue([JSONValue(0), JSONValue(2147483648)])])]),
]);
}
