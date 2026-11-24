#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
make_widget([dynamic]any{1}, [dynamic]any{"text"});
}
