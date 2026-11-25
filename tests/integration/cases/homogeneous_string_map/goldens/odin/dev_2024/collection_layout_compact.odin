#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = "x",
	"b" = "y",
}
_ = my_data
}
