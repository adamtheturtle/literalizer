import std.json;
void main() {
auto my_data = JSONValue([
    "date": JSONValue("0099-05-27"),
    "naive": JSONValue(-62135551800),
    "recent": JSONValue(1716804000),
]);
}
