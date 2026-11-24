#+feature dynamic-literals
package main
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := 42
consume(map[string]any{"field" = item});
}
