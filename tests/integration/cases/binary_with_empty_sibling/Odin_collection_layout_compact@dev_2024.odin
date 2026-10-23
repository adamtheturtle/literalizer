#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"48656c6c6f",
	[dynamic]any{},
}
_ = my_data
}
