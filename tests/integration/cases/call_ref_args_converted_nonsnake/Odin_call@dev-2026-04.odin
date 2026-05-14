#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_var := [dynamic]any{
	1,
	2,
	3,
}
my_other := [dynamic]any{
	4,
	5,
	6,
}
process(my_var, 42);
process(my_other, 7);
}
