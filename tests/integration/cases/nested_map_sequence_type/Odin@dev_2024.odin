#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{"b" = [dynamic]any{1, 2, 3}},
}
_ = my_data
}
