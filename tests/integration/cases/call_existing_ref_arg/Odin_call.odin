#+feature dynamic-literals
package main
send :: proc(args: ..any) -> any { return nil }

main :: proc() {
existing := 42
send(existing);
}
