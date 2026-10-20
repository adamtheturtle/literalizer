#+feature dynamic-literals
package main
_thing_go_ :: proc(args: ..any) -> any { return nil }
ThingType_ :: struct { go: proc(..any) -> any }

main :: proc() {
thing: ThingType_ = ThingType_{ go = _thing_go_ }
item := [dynamic]any{
	1,
	2,
}
thing.go(item);
}
