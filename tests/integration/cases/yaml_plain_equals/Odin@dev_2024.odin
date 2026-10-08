#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"x" = "=",
	// unrelated
}
_ = my_data
}
