#+feature dynamic-literals
package main
Record0 :: struct { quantity: int, big: u64, ratio: f64, label: string, ok: bool }

main :: proc() {
my_data := Record0{
	quantity = 0b11110100001001000000,
	big = 0b1111111111111111111111111111111111111111111111111111111111111111,
	ratio = 2.5,
	label = "tag",
	ok = true,
}
_ = my_data
}
