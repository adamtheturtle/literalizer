import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("C:\\path\\to\\file"),
    JSONValue("back\\\\slash"),
    JSONValue("hello \\\"world\\\""),
    JSONValue("path\\to \"# file"),
    JSONValue("trailing\\"),
    JSONValue("both \"quotes''' here"),
    JSONValue("line1\\nline2\nwith newline"),
]);
}
