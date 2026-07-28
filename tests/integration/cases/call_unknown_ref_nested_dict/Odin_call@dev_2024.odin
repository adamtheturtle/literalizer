#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_list := [dynamic]any{}
process([dynamic]any{[dynamic]any{map[string]any{"inner" = my_list}}});
}
