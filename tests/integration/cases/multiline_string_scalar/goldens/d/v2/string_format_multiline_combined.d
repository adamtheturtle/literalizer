import std.json;
void main() {
auto my_data = JSONValue(`
root first line
  indented

root last line
`);
my_data = JSONValue(`
root first line
  indented

root last line
`);
}
