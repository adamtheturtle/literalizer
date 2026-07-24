#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_var := 42
process(map[string]any{"key" = my_var, "count" = 42, "label" = "example"});
}
