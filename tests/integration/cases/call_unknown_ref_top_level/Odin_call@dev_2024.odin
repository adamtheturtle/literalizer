#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
unknown_value := [dynamic]any{
	1,
}
process(unknown_value);
}
