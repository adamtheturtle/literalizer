#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
x := [dynamic]any{
	[dynamic]any{
		1,
		2,
	},
	[dynamic]any{
		3,
		4,
	},
}
f([dynamic]any{
	[dynamic]any{
		x,
	},
});
}
