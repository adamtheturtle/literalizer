#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"id" = 1,
	"owner" = map[string]any{"name" = "Alice", "age" = 30},
}
_ = my_data
}
