#+feature dynamic-literals
package main

main :: proc() {
std := map[string]any{
	"a" = 1,
}
arena := map[string]any{
	"a" = 1,
}
allocator := map[string]any{
	"a" = 1,
}
my_data := [dynamic]any{
	std,
	arena,
	allocator,
}
_ = my_data
}
