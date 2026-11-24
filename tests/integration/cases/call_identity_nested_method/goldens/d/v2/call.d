import std.json;
void main() {
struct ThingType_ { int go(T...)(T args) { return 0; } }
struct OuterType_ { ThingType_ thing; }
OuterType_ outer;
outer.thing.go();
}
