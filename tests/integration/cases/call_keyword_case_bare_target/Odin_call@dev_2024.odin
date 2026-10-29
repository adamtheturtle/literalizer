#+feature dynamic-literals
package main
Before :: proc(args: ..any) -> any { return nil }

main :: proc() {
Before(1);
}
