#+feature dynamic-literals
package main
Record0 :: struct { a: int }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
stamp := "2001-02-03"
item := Record0{
	a = 1,
}
consume(stamp, item);
}
