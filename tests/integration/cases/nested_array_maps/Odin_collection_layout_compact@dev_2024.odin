#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"groups" = [dynamic]any{[dynamic]any{map[string]any{"id" = 1}}, [dynamic]any{map[string]any{"id" = 2}}},
}
_ = my_data
}
