#+feature dynamic-literals
package main
Record0 :: struct { name: string, values: [dynamic]any }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := Record0{
	name = "first",
	values = [dynamic]any{
		1,
		2,
	},
}
consume(item);
}
