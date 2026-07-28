#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
unknown_value := [dynamic]any{}
process(unknown_value);
}
