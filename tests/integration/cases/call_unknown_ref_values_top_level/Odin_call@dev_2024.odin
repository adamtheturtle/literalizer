#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
known_value := 1
unknown_value := [dynamic]any{}
process(unknown_value);
}
