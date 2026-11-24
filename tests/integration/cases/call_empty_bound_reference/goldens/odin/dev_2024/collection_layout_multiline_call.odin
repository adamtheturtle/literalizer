#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
items := [dynamic]any{}
make_widget(items);
}
