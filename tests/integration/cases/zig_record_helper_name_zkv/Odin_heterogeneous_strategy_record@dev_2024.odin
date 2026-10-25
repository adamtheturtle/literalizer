#+feature dynamic-literals
package main
Record0 :: struct { a: int }

main :: proc() {
ZKV := Record0{
	a = 1,
}
_ = ZKV
}
