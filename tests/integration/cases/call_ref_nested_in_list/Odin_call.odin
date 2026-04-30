#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_var := 42
my_other := 7
process([dynamic]any{my_var, 42, "static"});
process([dynamic]any{my_other, 7, "label"});
}
