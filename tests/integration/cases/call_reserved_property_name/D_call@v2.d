import std.json;
void main() {
struct FooType_ { int class(T...)(T args) { return 0; } }
FooType_ foo;
foo.class(1);
}
