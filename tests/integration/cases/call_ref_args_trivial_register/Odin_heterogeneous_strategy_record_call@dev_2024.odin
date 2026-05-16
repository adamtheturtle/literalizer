#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_int := 1
my_bool := true
my_float := 3.14
my_list := [dynamic]any{
	1,
	2,
	3,
}
process(my_int, 42);
process(my_bool, 7);
process(my_float, 9);
process(my_list, 1);
}
