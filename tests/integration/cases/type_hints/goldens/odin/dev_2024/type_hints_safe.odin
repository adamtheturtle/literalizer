#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"age" = 30,
	"active" = true,
	"score" = nil,
	"joined" = "2024-01-15",
	"last_login" = "2024-01-15T12:30:00+00:00",
	"avatar" = "48656c6c6f",
}
_ = my_data
}
