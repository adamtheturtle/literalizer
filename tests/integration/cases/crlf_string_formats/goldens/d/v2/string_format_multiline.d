import std.json;
void main() {
auto my_data = JSONValue([
    `x`: JSONValue("line1\r\nline2"),
]);
}
