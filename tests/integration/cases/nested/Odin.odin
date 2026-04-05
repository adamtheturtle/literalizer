#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"users" = [dynamic]any{map[string]any{"name" = "Bob", "tags" = [dynamic]any{"admin", "user"}}, map[string]any{"name" = "Carol", "tags" = [dynamic]any{"guest"}}},
}
_ = my_data
}
