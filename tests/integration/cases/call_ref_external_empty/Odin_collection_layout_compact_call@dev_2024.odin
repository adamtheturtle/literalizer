#+feature dynamic-literals
package main
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := [dynamic]any{
	1,
	2,
}
consume(item);
}
