#+feature dynamic-literals
package main
Record1 :: struct { a: int, b: string, c: any }
Record0 :: struct { outer: Record1 }

main :: proc() {
my_data := Record0{
	outer = Record1{
		a = 1,
		b = "x",
		c = nil,
	},
}
_ = my_data
}
