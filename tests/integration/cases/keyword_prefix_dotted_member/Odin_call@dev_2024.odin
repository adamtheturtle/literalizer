#+feature dynamic-literals
package main
_thing_first_value_ :: proc(args: ..any) -> any { return nil }
ThingType_ :: struct { first_value: proc(..any) -> any }

main :: proc() {
thing: ThingType_ = ThingType_{ first_value = _thing_first_value_ }
thing.first_value(1);
}
