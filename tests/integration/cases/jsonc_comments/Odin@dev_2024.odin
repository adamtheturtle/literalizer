#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"url" = "https://example.org/a/*b*/",
	"count" = 2,
}
_ = my_data
}
