#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"v" = "a‪\x00é😀b",
}
_ = my_data
}
