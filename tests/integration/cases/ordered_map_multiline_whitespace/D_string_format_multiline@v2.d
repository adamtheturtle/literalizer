import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(`  leading
key  `), JSONValue(`  leading
value
  `)]),
    JSONValue([JSONValue(`next
	key`), JSONValue([JSONValue(`
first
`), JSONValue(` last
 `)])]),
]);
}
