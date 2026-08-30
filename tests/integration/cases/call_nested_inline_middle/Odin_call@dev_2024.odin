#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
f([dynamic]any{[dynamic]any{"DEL", "b", "10"}, [dynamic]any{"ADD", "a", "x"}});  // note
// next call
f([dynamic]any{[dynamic]any{"ADD", "c", "y"}});
}
