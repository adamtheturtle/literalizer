import std.json;
void main() {
auto my_data = JSONValue([
    "a_b": JSONValue(0b1),
    "a-b": JSONValue(0b10),
    "averyveryverylongkeynamethatgoesonandonandon": JSONValue(0b11),
    "averyveryverylongkeynamethatgoesonandmore": JSONValue(0b100),
]);
}
