#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"tags" = map[string]struct{}{"42" = {}, "True" = {}, "apple" = {}},
}
_ = my_data
}
