#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"reference" = "whole",
}
_ = my_data
}
