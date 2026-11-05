#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := (make_widget([dynamic]any{1, 2}) != nil ?
make_widget([dynamic]any{1, 2}) \
 // inner
: nil) // trailing
_ = my_data
}
