#+feature dynamic-literals
package main
Record0 :: struct { within_i32: int, beyond_i32: int }

main :: proc() {
my_data := Record0{
	within_i32 = 1705320000,
	beyond_i32 = 4085195400,
}
_ = my_data
}
