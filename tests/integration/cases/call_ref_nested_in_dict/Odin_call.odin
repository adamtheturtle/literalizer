#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_var := 42
process(map[string]any{"key" = map[string]any{"ref" = "my_var"}, "count" = 42});
}
