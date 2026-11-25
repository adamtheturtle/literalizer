#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process("Dune");  // first edition
process("Solaris");
process("Neuromancer");  // cyberpunk
}
