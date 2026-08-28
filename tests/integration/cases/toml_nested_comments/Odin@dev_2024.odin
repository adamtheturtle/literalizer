#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// About the first dotted key.
	// About the second dotted key.
	"dotted" = map[string]any{"first" = 1, "second" = 2},
	"plain" = 3,  // About the plain key.
	// Before the first entry.
	// Before the second entry.
	"entries" = [dynamic]any{map[string]any{"name" = "one"}, map[string]any{"name" = "two"}},
	// Inside the table.
	"table" = map[string]any{"inner" = 4},
}
_ = my_data
}
