#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"score" = nil,
	"age" = 30,
}
_ = my_data
}
