import std.json;
void main() {
auto my_data = JSONValue([
    "a_b": JSONValue(1),
    "a-b": JSONValue(2),
    "averyveryverylongkeynamethatgoesonandonandon": JSONValue(3),
    "averyveryverylongkeynamethatgoesonandmore": JSONValue(4),
]);
my_data = JSONValue([
    "a_b": JSONValue(1),
    "a-b": JSONValue(2),
    "averyveryverylongkeynamethatgoesonandonandon": JSONValue(3),
    "averyveryverylongkeynamethatgoesonandmore": JSONValue(4),
]);
}
