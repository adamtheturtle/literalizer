#+feature dynamic-literals
package main
Record0 :: struct { quantity: int, big: u64, ratio: f64, label: string, ok: bool }

main :: proc() {
my_data := Record0{
	quantity = 0xf4240,
	big = 0xffffffffffffffff,
	ratio = 2.5,
	label = "tag",
	ok = true,
}
_ = my_data
}
