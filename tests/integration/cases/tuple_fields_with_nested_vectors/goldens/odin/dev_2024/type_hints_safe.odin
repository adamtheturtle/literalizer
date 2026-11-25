#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"lint" = [dynamic]any{2, [dynamic]any{}},
	"test" = [dynamic]any{5, [dynamic]any{"compile"}},
	"package" = [dynamic]any{7, [dynamic]any{"link", "test"}},
}
_ = my_data
}
