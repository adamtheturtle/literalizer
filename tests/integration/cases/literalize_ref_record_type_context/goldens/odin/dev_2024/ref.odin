#+feature dynamic-literals
package main
Record1 :: struct { x: string }
Record2 :: struct { x: int }
Record0 :: struct { direct: Record1, bound: Record2 }

main :: proc() {
first := Record2{
	x = 1,
}
my_data := Record0{
	direct = Record1{
		x = "s",
	},
	bound = first,
}
_ = my_data
}
