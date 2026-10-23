#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o1,
	"hello",
	true,
	nil,
}
_ = my_data
}
