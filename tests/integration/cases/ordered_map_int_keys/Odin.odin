#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"1" = "one",
	"2" = "two",
	"42" = "answer",
}
_ = my_data
}
