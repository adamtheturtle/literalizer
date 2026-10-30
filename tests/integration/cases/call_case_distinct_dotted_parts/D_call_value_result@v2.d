import std.json;
void main() {
struct FooType_2 { int bar(T...)(T args) { return 0; } }
struct FooType_1 { FooType_2 Foo; }
struct AType_ { FooType_1 foo; }
AType_ a;
auto my_data = a.foo.Foo.bar(JSONValue([JSONValue(1)]));
}
