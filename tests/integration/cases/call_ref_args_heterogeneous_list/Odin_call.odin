#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_ints := [dynamic]any{
	1,
	2,
	3,
}
my_strings := [dynamic]any{
	"a",
	"b",
}
process(my_ints, 42);
process(my_strings, 7);
}
