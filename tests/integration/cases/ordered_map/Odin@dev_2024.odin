#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"age" = 30,
	"active" = true,
}
_ = my_data
}
