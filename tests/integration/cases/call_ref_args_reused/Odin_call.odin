#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
shared := 1
other := 2
process(shared, 1);
process(other, 0);
process(shared, 8);
}
