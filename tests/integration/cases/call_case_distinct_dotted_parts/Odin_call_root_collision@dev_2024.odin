#+feature dynamic-literals
package main
_Foo_bar_ :: proc(args: ..any) -> any { return nil }
FooType_1 :: struct { bar: proc(..any) -> any }
FooType_0 :: struct { Foo: FooType_1 }

main :: proc() {
foo: FooType_0 = FooType_0{ Foo = FooType_1{ bar = _Foo_bar_ } }
foo.Foo.bar([dynamic]any{1});
}
