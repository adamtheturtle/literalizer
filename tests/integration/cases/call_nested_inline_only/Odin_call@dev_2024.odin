#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
f(2, "hello");  // trailing note
f(3, "world");  // another note
}
