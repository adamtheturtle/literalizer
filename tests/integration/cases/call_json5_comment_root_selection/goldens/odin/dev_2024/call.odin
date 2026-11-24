#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
// selected heading
f(1, 2);  // selected inline
}
