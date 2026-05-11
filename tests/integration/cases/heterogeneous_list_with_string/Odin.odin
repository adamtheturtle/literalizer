#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"hello",
	42,
}
_ = my_data
}
