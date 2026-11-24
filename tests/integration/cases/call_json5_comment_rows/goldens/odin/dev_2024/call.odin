#+feature dynamic-literals
package main
f :: proc(args: ..any) -> any { return nil }

main :: proc() {
// calls heading
// before call one
// first argument
f(1, 2);  // after call one
// second argument
f(3, 4);
// after all calls
}
