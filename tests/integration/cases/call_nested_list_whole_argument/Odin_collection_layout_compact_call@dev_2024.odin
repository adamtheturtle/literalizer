#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
f([dynamic]any{[dynamic]any{1, 2}, [dynamic]any{3}});
}
