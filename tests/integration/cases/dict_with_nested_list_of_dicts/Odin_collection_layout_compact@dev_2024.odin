#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{[dynamic]any{map[string]any{"b" = 1}}},
}
_ = my_data
}
