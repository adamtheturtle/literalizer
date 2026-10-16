#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42);
}
