import std.json;
void main() {
    auto my_data = JSONValue(`
first line
  indented

last line
`);
    assert(my_data.str == "\nfirst line\n  indented\n\nlast line\n");
}
