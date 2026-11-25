#+feature dynamic-literals
package main
_thing_go_ :: proc(args: ..any) -> any { return nil }
ThingType_ :: struct { go: proc(..any) -> any }

main :: proc() {
thing: ThingType_ = ThingType_{ go = _thing_go_ }
thing.go([dynamic]any{}, [dynamic]any{1}, [dynamic]any{});
thing.go([dynamic]any{"text"}, [dynamic]any{2}, [dynamic]any{});
thing.go([dynamic]any{}, [dynamic]any{"text"}, [dynamic]any{});
thing.go([dynamic]any{"text"}, [dynamic]any{2}, [dynamic]any{3});
}
