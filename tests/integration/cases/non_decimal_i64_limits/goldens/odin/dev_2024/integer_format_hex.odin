#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0x8000000000000000,
	-0x1,
	0x7fffffffffffffff,
}
_ = my_data
}
