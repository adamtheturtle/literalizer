#+feature dynamic-literals
package main
put :: proc(args: ..any) -> any { return nil }
get :: proc(args: ..any) -> any { return nil }

main :: proc() {
put(1, 10);
get(1);
}
