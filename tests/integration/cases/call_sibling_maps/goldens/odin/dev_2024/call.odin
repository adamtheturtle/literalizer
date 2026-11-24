#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process(map[string]any{"value" = 1});
process(map[string]any{"value" = "hello"});
}
