#+feature dynamic-literals
package main
record :: proc(args: ..any) -> any { return nil }
flush :: proc(args: ..any) -> any { return nil }

main :: proc() {
record(42);
flush(3);
}
