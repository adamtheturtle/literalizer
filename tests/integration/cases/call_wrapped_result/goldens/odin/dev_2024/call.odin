#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(1)
_ = my_data
}
