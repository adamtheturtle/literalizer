#+feature dynamic-literals
package main
_fooBar_bar_ :: proc(args: ..any) -> any { return nil }
FoobarType_ :: struct { bar: proc(..any) -> any }
Foo_BarType_ :: struct { fooBar: FoobarType_ }
AType_ :: struct { foo_bar: Foo_BarType_ }

main :: proc() {
a: AType_ = AType_{ foo_bar = Foo_BarType_{ fooBar = FoobarType_{ bar = _fooBar_bar_ } } }
a.foo_bar.fooBar.bar([dynamic]any{1});
}
