#+feature dynamic-literals
package main
Record0 :: struct { quantity: int, big: u64, ratio: f64, label: string, ok: bool }

main :: proc() {
my_data := Record0{
	quantity = 1_000_000,
	big = 18_446_744_073_709_551_615,
	ratio = 2.5,
	label = "tag",
	ok = true,
}
_ = my_data
}
