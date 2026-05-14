#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"user" = map[string]any{"id" = 1, "name" = "Alice"},
	"project" = map[string]any{"title" = "report", "tags" = [dynamic]any{"draft", "urgent"}},
}
_ = my_data
}
