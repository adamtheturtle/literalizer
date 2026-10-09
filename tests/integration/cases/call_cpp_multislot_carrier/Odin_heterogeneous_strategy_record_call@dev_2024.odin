#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process(1, "hello");
process("two", false);
process(3.5, nil);
}
