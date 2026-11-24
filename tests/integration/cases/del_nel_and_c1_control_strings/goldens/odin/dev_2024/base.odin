#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"del" = "ab",
	"nel" = "ab",
	"c1" = "ab",
}
_ = my_data
}
