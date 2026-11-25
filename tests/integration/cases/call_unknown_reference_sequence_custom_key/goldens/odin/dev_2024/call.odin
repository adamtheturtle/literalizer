#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
untyped_value := [dynamic]any{}
process([dynamic]any{untyped_value, untyped_value});
}
