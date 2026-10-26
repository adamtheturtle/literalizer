#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }
repr :: proc(args: ..any) -> any { return nil }

main :: proc() {
ref_data := 1
repr(f(ref_data));
}
