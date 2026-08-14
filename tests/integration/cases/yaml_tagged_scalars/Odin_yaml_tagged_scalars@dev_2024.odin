#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"explicit_string" = "5",
	"six" = "explicitly tagged key",
}
_ = my_data
}
