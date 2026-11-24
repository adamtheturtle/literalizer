#+feature dynamic-literals
package main
_thing_Before_ :: proc(args: ..any) -> any { return nil }
ThingType_ :: struct { Before: proc(..any) -> any }

main :: proc() {
thing: ThingType_ = ThingType_{ Before = _thing_Before_ }
thing.Before(1);
}
