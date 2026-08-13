#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"]",
	"a]",
	"a]=",
	"a]b",
}
_ = my_data
}
