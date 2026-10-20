#+feature dynamic-literals
package main
Record1 :: struct { value: int }
Record0 :: struct { child: Record1 }

main :: proc() {
first := Record0{
	child = Record1{
		value = 1,
	},
}
my_data := first
_ = my_data
}
