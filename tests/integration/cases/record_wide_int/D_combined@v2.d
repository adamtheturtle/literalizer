import std.json;
void main() {
auto my_data = JSONValue([
    "quantity": JSONValue(1000000),
    "big": JSONValue(18446744073709551615),
    "ratio": JSONValue(2.5),
    "label": JSONValue("tag"),
    "ok": JSONValue(true),
]);
my_data = JSONValue([
    "quantity": JSONValue(1000000),
    "big": JSONValue(18446744073709551615),
    "ratio": JSONValue(2.5),
    "label": JSONValue("tag"),
    "ok": JSONValue(true),
]);
}
