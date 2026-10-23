#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{},
	"b" = [dynamic]any{},
}
_ = my_data
}
