import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("\nfirst line\n  indented\n\nlast line\n")]),
]);
}
