#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	"hello",
	true,
}
_ = my_data
}
