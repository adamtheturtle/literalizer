#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := (~/\//).match("/") ? make_widget(42) : null // trailing
_ = my_data
}
