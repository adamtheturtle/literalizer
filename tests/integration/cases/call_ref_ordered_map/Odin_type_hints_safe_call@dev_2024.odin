#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
big_list := [dynamic]any{
	"x",
}
process(map[string]any{"m" = big_list});
}
