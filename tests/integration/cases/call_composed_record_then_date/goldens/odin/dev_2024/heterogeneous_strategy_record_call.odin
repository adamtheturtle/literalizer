#+feature dynamic-literals
package main
Record0 :: struct { a: int }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := Record0{
	a = 1,
}
stamp := "2001-02-03"
consume(stamp, item);
}
