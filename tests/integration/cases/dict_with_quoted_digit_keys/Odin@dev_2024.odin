#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"0a" = "first",
	"1b" = "second",
}
_ = my_data
}
