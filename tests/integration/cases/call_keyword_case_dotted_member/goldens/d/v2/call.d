import std.json;
void main() {
struct ThingType_ { int Before(T...)(T args) { return 0; } }
ThingType_ thing;
thing.Before(1);
}
