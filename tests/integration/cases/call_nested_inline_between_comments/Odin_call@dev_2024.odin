#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
f(2, "hello");  // trailing note
// next element
f(3, "world");
}
