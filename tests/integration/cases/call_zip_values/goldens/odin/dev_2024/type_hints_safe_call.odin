#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
emit(process("hello"), true);
emit(process(42), false);
}
