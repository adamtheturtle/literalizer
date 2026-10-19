import std.json;
void main() {
auto text = JSONValue("a\u202Ab");
auto my_data = JSONValue([
    "value": text,
]);
}
