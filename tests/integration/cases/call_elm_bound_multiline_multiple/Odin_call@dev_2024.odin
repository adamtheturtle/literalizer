#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
ref_data := [dynamic]any{
	1,
	2,
}
f([dynamic]any{
	ref_data,
});
f([dynamic]any{
	ref_data,
});
}
