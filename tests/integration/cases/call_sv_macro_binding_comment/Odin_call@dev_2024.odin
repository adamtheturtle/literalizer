#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := (`__LINE__ > 0) ? make_widget(42) : make_widget(42) // trailing `marker
_ = my_data
}
