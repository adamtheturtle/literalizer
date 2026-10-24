#+feature dynamic-literals
package main
Record1 :: struct { integer: int, boolean: bool, decimal: f64, null: any }
Record3 :: struct { integer: int }
Record2 :: struct { child: Record3 }
Record4 :: struct { text: string }
Record5 :: struct { day: string, stamp: string }
Record0 :: struct { trivial: Record1, nested: Record2, owning: Record4, calendar: Record5 }

main :: proc() {
trivial := Record1{
	integer = 1,
	boolean = true,
	decimal = 1.5,
	null = nil,
}
nested := Record2{
	child = Record3{
		integer = 2,
	},
}
owning := Record4{
	text = "owned",
}
calendar := Record5{
	day = "2001-01-02",
	stamp = "2001-01-02T03:04:05+00:00",
}
my_data := Record0{
	trivial = trivial,
	nested = nested,
	owning = owning,
	calendar = calendar,
}
_ = my_data
}
