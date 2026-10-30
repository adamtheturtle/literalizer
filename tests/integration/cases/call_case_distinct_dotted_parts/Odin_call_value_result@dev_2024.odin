#+feature dynamic-literals
package main
_Foo_bar_ :: proc(args: ..any) -> any { return nil }
FooType_2 :: struct { bar: proc(..any) -> any }
FooType_1 :: struct { Foo: FooType_2 }
AType_ :: struct { foo: FooType_1 }

main :: proc() {
a: AType_ = AType_{ foo = FooType_1{ Foo = FooType_2{ bar = _Foo_bar_ } } }
my_data := a.foo.Foo.bar([dynamic]any{1})
_ = my_data
}
