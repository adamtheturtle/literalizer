#+feature dynamic-literals
package main
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
foo := 42
consume([dynamic]any{
	map[string]any{
		"other" = 1,
	},
	foo,
}, map[string]any{
	"left" = foo,
	"other" = 1,
});
}
