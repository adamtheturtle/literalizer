#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{1, [dynamic]any{2}, [dynamic]any{2}},
}
_ = my_data
}
