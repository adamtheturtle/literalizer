#+feature dynamic-literals
package main
_foo_class_ :: proc(args: ..any) -> any { return nil }
FooType_ :: struct { class: proc(..any) -> any }

main :: proc() {
foo: FooType_ = FooType_{ class = _foo_class_ }
foo.class(1);
}
