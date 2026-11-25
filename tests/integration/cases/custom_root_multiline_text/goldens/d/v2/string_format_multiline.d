import std.json;
void main() {
auto custom_data = JSONValue(`head
final my_data = 123;
final fakeRoot = 1;
final fixtureRoot = 1;
tail`);
}
