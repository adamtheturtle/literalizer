#+feature dynamic-literals
package main
_thing_go_ :: proc(args: ..any) -> any { return nil }
ThingType_ :: struct { go: proc(..any) -> any }

main :: proc() {
thing: ThingType_ = ThingType_{ go = _thing_go_ }
my_data := thing.go([dynamic]any{})
_ = my_data
}
