#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"age" = 0o36,
	"active" = true,
}
_ = my_data
}
