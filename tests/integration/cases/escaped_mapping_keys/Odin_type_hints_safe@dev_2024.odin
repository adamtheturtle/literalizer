#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"quote\"backslash\\" = 1,
	"line\nbreak" = 2,
	"$(literal)${text}" = 3,
	"RStr prefix" = 4,
}
_ = my_data
}
