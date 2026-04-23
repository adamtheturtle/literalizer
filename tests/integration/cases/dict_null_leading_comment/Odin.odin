#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// comment
	"name" = "Alice",
	"score" = nil,
}
_ = my_data
}
