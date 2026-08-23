#+feature dynamic-literals
package main
self :: proc(args: ..any) -> any { return nil }

main :: proc() {
self("hello");
}
