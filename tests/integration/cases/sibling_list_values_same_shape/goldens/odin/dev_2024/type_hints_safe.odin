#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"test" = [dynamic]any{5, [dynamic]any{"compile", "test"}},
	"package" = [dynamic]any{7, [dynamic]any{"link", "test"}},
}
_ = my_data
}
