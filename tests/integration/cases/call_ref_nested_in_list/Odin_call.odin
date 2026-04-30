#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_var := 42
my_other := 7
process([dynamic]any{map[string]any{"ref" = "my_var"}, 42, "static"});
process([dynamic]any{map[string]any{"ref" = "my_other"}, 7, "label"});
}
