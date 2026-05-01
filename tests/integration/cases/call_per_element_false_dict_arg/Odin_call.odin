#+feature dynamic-literals
package main
send :: proc(args: ..any) -> any { return nil }

main :: proc() {
send(map[string]any{"a" = 1, "b" = "x"});
}
