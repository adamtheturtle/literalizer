#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"input" = map[string]any{"name" = "alice", "city" = "paris"}, "expected" = map[string]any{"count" = 1, "total" = 2}},
	map[string]any{"input" = map[string]any{"name" = 10, "city" = 20}, "expected" = map[string]any{"count" = "done", "total" = "pending"}},
}
_ = my_data
}
