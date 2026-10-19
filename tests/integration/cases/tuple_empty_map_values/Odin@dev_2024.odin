#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"filled" = [dynamic]any{1, "value"},
	"empty" = [dynamic]any{},
}
_ = my_data
}
