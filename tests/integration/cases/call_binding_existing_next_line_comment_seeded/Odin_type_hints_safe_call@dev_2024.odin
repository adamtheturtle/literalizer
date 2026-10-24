#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(42)
consume_widget(my_data);
my_data = make_widget(my_data)
// note
consume_widget(my_data);
}
