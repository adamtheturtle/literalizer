#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"comma_hash" = "a,#b",
	"comma_space_hash" = "trail, # comment",
	"escaped_quote" = "quote \" and , #",
	"next_line" = "xy",
	"line_separator" = "x y",
	"paragraph_separator" = "x y",
}
_ = my_data
}
