#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"age" = 0b11110,
	"active" = true,
}
_ = my_data
}
