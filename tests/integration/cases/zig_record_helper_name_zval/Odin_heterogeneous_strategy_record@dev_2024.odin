#+feature dynamic-literals
package main
Record0 :: struct { a: int }

main :: proc() {
ZVal := Record0{
	a = 1,
}
_ = ZVal
}
