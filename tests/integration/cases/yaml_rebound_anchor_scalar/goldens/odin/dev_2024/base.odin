#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{1, 2, 2},
}
_ = my_data
}
