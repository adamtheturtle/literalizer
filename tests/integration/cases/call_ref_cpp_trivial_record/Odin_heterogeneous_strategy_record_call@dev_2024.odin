#+feature dynamic-literals
package main
Record0 :: struct { value: int }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := Record0{
	value = 1,
}
consume(item);
}
