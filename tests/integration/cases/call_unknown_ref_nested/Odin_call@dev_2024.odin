#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
known_value := true
unknown_value := true
process(known_value, unknown_value);
}
