#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"text" = "a\"//b",
}
_ = my_data
}
