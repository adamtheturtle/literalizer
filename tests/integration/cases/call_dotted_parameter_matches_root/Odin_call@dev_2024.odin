#+feature dynamic-literals
package main
_outer_inner_ :: proc(args: ..any) -> any { return nil }
OuterType_ :: struct { inner: proc(..any) -> any }

main :: proc() {
outer: OuterType_ = OuterType_{ inner = _outer_inner_ }
outer.inner(1, 2);
}
