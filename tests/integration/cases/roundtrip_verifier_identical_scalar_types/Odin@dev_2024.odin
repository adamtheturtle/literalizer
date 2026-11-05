#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"value" = [dynamic]any{true, false, 0, 1},
}
_ = my_data
}
