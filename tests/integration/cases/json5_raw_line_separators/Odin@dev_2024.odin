#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"double" = "a b",
	"single" = "c d",
	"both" = "e f g",
	"continued" = "hi",
	"escaped backslash" = "j\\ k",
}
_ = my_data
}
