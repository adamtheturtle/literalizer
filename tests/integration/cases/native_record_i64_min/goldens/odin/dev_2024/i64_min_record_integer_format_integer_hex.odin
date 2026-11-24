#+feature dynamic-literals
package main
Record0 :: struct { value: int }

main :: proc() {
my_data := Record0{
	value = -0x8000000000000000,
}
_ = my_data
}
