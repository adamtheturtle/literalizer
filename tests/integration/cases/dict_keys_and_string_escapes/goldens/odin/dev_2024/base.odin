#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"plain" = [dynamic]any{1, 2},
	"with-dash" = "a\nb",
}
_ = my_data
}
