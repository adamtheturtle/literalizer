#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"x" = "\ufeff",
}
_ = my_data
}
