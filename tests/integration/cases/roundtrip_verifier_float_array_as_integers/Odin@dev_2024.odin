#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"value" = [dynamic]any{0, 1},
}
_ = my_data
}
