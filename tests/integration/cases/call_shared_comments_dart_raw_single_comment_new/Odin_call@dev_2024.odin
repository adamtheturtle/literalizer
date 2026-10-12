#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := (r'ends\' + '// payload').length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra
_ = my_data
}
