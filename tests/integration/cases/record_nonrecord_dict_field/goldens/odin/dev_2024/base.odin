#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"label" = "tag",
	"meta" = map[string]any{},
}
_ = my_data
}
