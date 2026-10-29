import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(0x0.0000000000001p-1022),
    JSONValue(2.2250738585072014e-308),
    JSONValue(1.0e-307),
    JSONValue(1.0e21),
    JSONValue(-1.5e300),
    JSONValue(1.7976931348623157e308),
    JSONValue(-1.7976931348623157e308),
]);
}
