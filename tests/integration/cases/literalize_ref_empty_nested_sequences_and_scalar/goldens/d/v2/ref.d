import std.json;
void main() {
auto seed = JSONValue(1);
auto my_data = JSONValue([
    parseJSON("[]"),
    JSONValue([parseJSON("[]")]),
    seed,
]);
}
