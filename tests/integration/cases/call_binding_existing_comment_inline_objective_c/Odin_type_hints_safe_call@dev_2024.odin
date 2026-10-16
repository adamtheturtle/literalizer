#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(42)
make_widget(my_data);
my_data = make_widget(my_data) // note
make_widget(my_data);
}
