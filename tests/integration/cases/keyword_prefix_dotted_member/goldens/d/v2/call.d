import std.json;
void main() {
struct ThingType_ { int first_value(T...)(T args) { return 0; } }
ThingType_ thing;
thing.first_value(1);
}
