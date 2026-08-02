import std.json;
void main() {
auto my_data = JSONValue(`first line
  indented

last line`);
my_data = JSONValue(`first line
  indented

last line`);
}
