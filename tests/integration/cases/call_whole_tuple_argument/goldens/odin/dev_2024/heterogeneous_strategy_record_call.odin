#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process([dynamic]any{"hello", 42, true});
}
