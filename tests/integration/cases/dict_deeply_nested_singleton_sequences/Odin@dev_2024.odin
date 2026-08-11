#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"deep" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{1}}}},
}
_ = my_data
}
