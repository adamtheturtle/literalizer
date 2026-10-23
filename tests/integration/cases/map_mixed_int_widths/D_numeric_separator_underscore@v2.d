import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue(1_099_511_627_776),
]);
}
