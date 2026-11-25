#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"price $10",
	"$HOME",
}
_ = my_data
}
