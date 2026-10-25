#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(nil)
consume(my_data);
my_data = make_widget(42) // note
consume(my_data);
}
