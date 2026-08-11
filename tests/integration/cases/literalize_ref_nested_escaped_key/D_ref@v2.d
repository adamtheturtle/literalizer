import std.json;
void main() {
auto foo = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    "items": JSONValue([JSONValue(["other": JSONValue(1)]), foo]),
    "mapping": JSONValue(["value": foo]),
]);
}
