#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"message" = "no comment here",
}
_ = my_data
}
