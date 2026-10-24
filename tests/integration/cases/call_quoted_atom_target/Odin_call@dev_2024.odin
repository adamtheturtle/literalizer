#+feature dynamic-literals
package main
DoThing :: proc(args: ..any) -> any { return nil }

main :: proc() {
DoThing(1);
DoThing(2);
}
