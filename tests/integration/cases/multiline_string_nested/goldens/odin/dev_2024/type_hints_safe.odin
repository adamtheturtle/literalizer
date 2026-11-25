#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"outer" = [dynamic]any{[dynamic]any{"nested first line\n  indented\n\nnested last line\n"}},
}
_ = my_data
}
