#+feature dynamic-literals
package main
record_value :: proc(args: ..any) -> any { return nil }
flush_buffer :: proc(args: ..any) -> any { return nil }
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
emit(record_value(42));
flush_buffer(3);
}
