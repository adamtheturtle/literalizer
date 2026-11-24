#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"first" = "one",
	"second" = "two",
	"third" = "three",
}
_ = my_data
}
