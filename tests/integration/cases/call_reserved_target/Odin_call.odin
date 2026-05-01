#+feature dynamic-literals
package main
op :: proc(args: ..any) -> any { return nil }

main :: proc() {
op("hello");
}
