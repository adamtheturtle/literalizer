#+feature dynamic-literals
package main
Record0 :: struct { value: string }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := Record0{
	value = "owned",
}
consume(item);
}
