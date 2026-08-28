#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process([dynamic]any{
	1,
	2,
});
process([dynamic]any{
	3,
});
}
