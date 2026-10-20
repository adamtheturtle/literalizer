import std.json;
void main() {
struct ThingType_ { int go(T...)(T args) { return 0; } }
ThingType_ thing;
auto item = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
thing.go(item);
}
