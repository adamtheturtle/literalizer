#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"v" = "ab",
	"ab" = 1,
}
_ = my_data
}
