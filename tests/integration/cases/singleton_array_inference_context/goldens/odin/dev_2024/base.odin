#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"nil" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{nil}}}}}}}}},
	"empty" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{}}}}}}}}}},
	"siblings" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{4, 5}}}}}}}}}},
}
_ = my_data
}
