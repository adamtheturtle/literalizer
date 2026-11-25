#+feature dynamic-literals
package main
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
external_value := 1
consume(external_value);
}
