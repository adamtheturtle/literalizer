#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
value := 1
make_widget(value);
}
