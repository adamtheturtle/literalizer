import std.json;
void main() {
auto my_data = JSONValue([
    `outer`: JSONValue([JSONValue([JSONValue(`nested first line
  indented

nested last line
`)])]),
]);
}
