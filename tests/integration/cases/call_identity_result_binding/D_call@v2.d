import std.json;
void main() {
struct ThingType_ { int go(T...)(T args) { return 0; } }
ThingType_ thing;
auto my_data = thing.go(parseJSON("[]"));
}
