#+feature dynamic-literals
package main
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
consume(-2147483649);
consume(2147483648);
}
