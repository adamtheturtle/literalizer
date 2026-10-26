#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := (make_widget(7) != nil ?
make_widget(7) \
 // inner
: nil) // trailing
_ = my_data
}
