#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process(1);  // note<U+2028>still commented<U+2029>done
}
