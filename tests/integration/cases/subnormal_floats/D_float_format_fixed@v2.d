import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(0x0.0000000000001p-1022),
    JSONValue(-0x0.0000000000001p-1022),
    JSONValue(0x0.012688b70e62bp-1022),
]);
}
