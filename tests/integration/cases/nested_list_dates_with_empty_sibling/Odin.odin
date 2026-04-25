#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{"2026-01-01", "2026-01-02"},
	[dynamic]any{},
	[dynamic]any{"2026-02-03", "2026-02-04"},
}
_ = my_data
}
