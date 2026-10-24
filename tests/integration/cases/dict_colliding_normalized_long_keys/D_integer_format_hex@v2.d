import std.json;
void main() {
auto my_data = JSONValue([
    "a_b": JSONValue(0x1),
    "a-b": JSONValue(0x2),
    "averyveryverylongkeynamethatgoesonandonandon": JSONValue(0x3),
    "averyveryverylongkeynamethatgoesonandmore": JSONValue(0x4),
]);
}
