import std.json;
void main() {
auto my_data = JSONValue([
    "a-b": JSONValue(1),
    "two words": JSONValue(2),
    "she said \"hi\"": JSONValue(3),
    "": JSONValue(4),
    "valid_key": JSONValue(5),
]);
}
