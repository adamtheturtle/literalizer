#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"x" = "",
}
_ = my_data
}
