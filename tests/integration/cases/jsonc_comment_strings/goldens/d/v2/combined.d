import std.json;
void main() {
auto my_data = JSONValue([
    // strings stay data
    JSONValue("https://example.org/a/*b*/"),  // URL annotation
    JSONValue("escaped quote: \" // still data"),
    JSONValue("backslash: \\"),  // outside the string
    JSONValue("/* not a comment */"),
]);
my_data = JSONValue([
    // strings stay data
    JSONValue("https://example.org/a/*b*/"),  // URL annotation
    JSONValue("escaped quote: \" // still data"),
    JSONValue("backslash: \\"),  // outside the string
    JSONValue("/* not a comment */"),
]);
}
