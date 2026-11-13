import std.json;
void main() {
struct FoobarType_ { int bar(T...)(T args) { return 0; } }
struct Foo_BarType_ { FoobarType_ fooBar; }
struct AType_ { Foo_BarType_ foo_bar; }
AType_ a;
a.foo_bar.fooBar.bar(JSONValue([JSONValue(1)]));
}
