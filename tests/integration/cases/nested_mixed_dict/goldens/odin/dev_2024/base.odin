#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"outer" = map[string]any{"a" = 1, "b" = "x", "c" = nil},
}
_ = my_data
}
