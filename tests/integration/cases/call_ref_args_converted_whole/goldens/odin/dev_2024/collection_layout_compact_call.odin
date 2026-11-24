#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_var := [dynamic]any{
	1,
	2,
	3,
}
process(my_var);
}
