#+feature dynamic-literals
package main
Record1 :: struct { x: int }
Record2 :: struct { day: string, stamp: string }
Record0 :: struct { plain: Record1, timed: Record2 }

main :: proc() {
plain := Record1{
	x = 1,
}
timed := Record2{
	day = "2001-01-02",
	stamp = "2001-01-02T03:04:05+00:00",
}
my_data := Record0{
	plain = plain,
	timed = timed,
}
_ = my_data
}
