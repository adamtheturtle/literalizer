#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget([dynamic]any{[dynamic]any{1, 2}, [dynamic]any{3}})
_ = my_data
}
