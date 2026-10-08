import std.json;
void main() {
struct OuterType_ { int inner(T...)(T args) { return 0; } }
OuterType_ outer;
outer.inner(1, 2);
}
