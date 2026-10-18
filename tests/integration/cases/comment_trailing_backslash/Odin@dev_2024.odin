#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// comment ending backslash \ .
	"x" = 1,
}
_ = my_data
}
