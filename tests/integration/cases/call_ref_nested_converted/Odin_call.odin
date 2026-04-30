#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_var := 42
process([dynamic]any{map[string]any{"ref" = "myVar"}, 42, "static"});
}
