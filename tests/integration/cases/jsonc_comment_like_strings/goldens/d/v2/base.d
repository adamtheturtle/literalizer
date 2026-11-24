import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("// data"),
    JSONValue("/* data */"),
    JSONValue("escaped quote: \" // data"),
    JSONValue("backslash: \\"),
]);
}
