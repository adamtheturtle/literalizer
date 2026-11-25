import std.json;
void main() {
auto my_data = JSONValue([
    "label": JSONValue("tag"),
    "meta": parseJSON("{}"),
]);
}
