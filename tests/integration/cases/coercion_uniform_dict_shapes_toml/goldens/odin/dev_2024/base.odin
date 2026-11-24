#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"_" = [dynamic]any{map[string]any{"type" = "create", "name" = "a"}, map[string]any{"type" = "update", "name" = "b"}},
}
_ = my_data
}
