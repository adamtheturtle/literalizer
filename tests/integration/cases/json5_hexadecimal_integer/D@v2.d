import std.json;
void main() {
auto my_data = JSONValue([
    "lower": JSONValue(3735928559),
    "upper": JSONValue(31),
    "negative": JSONValue(-16),
    "zero": JSONValue(0),
]);
}
