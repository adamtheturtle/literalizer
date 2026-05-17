#+feature dynamic-literals
package main
Record1 :: struct { count: int, rate: int }
Record2 :: struct { retries: int, timeout: int }
Record0 :: struct { metrics: Record1, flags: Record2 }

main :: proc() {
my_data := Record0{
	metrics = Record1{
		count = 100,
		rate = 50,
	},
	flags = Record2{
		retries = 3,
		timeout = 30,
	},
}
_ = my_data
}
