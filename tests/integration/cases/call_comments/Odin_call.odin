#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
// Test cases
process("hello");  // single word
process("hello world");  // two words
// trailing comment
}
