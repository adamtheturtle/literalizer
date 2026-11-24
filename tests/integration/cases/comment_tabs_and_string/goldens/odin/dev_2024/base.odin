#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// before	line
	"value" = "left\tright",  // inline	line
	// after	line
}
_ = my_data
}
