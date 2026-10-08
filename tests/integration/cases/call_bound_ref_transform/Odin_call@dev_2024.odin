#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
ref_data := 1
f(ref_data);
}
