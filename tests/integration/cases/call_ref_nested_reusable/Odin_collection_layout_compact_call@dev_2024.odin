#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := [dynamic]any{
	1,
	2,
}
process([dynamic]any{item, item});
}
