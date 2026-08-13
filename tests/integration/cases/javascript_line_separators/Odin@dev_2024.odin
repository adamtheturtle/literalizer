#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"a b c",
	"a\r b",
}
_ = my_data
}
