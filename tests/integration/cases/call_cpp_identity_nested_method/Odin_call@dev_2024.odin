#+feature dynamic-literals
package main
_thing_go_ :: proc(args: ..any) -> any { return nil }
ThingType_ :: struct { go: proc(..any) -> any }
OuterType_ :: struct { thing: ThingType_ }

main :: proc() {
outer: OuterType_ = OuterType_{ thing = ThingType_{ go = _thing_go_ } }
outer.thing.go();
}
