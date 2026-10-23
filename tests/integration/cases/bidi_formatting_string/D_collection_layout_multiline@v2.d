import std.json;
void main() {
auto my_data = JSONValue([
    "v": JSONValue("a\u202A\u202B\u202C\u202D\u202E\u2066\u2067\u2068\u2069b"),
]);
}
