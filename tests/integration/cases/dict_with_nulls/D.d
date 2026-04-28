import std.json;
void main() {
auto my_data = JSONValue([
    "name": JSONValue("Alice"),
    "score": JSONValue(null),
    "age": JSONValue(30),
]);
}
