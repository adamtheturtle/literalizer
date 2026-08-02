import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(`first line
  indented

last line`)]),
]);
}
