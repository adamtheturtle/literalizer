#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(7)
consume(my_data);
my_data = (make_widget(13) != nil ?
make_widget(13) \
 // inner
: nil) // trailing
consume(my_data);
}
