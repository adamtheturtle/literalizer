#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// event time
	"when" = "2024-01-15T12:34:56+00:00",
}
_ = my_data
}
