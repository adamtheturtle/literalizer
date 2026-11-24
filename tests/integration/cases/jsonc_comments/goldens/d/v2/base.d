import std.json;
void main() {
auto my_data = JSONValue([
    // A JSONC input case with both comment forms.
    "url": JSONValue("https://example.org/a/*b*/"),  // detail
    // continued
    "count": JSONValue(2),  // trailing line comment
]);
}
