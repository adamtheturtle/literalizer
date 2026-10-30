import std.json;
void main() {
struct FooType_1 { int bar(T...)(T args) { return 0; } }
struct FooType_0 { FooType_1 Foo; }
FooType_0 foo;
foo.Foo.bar(JSONValue([JSONValue(1)]));
}
