#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
repeated_var := 1
single_var := [dynamic]any{
	4,
	5,
	6,
}
process(repeated_var, 1);
process(single_var, 0);
process(repeated_var, 8);
}
