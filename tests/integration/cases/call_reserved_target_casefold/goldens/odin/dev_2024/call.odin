#+feature dynamic-literals
package main
BEGIN :: proc(args: ..any) -> any { return nil }

main :: proc() {
BEGIN(42);
}
