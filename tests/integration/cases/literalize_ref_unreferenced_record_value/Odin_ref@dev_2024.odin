#+feature dynamic-literals
package main

main :: proc() {
other := "true"
my_data := map[string]any{
	"main" = map[string]any{"x" = 1, "y" = "s"},
}
_ = my_data
}
