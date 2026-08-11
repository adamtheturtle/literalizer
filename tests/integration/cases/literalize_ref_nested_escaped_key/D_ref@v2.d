import std.json;
void main() {
auto foo = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    "mapping": JSONValue(["value": foo]),
    "items": JSONValue([JSONValue(["other": JSONValue(1)]), foo]),
]);
}
