#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"_" = [dynamic]any{1, 2, 3},
}
_ = my_data
}
