#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(0)
consume_widget(my_data);
my_data = make_widget(1)
consume_widget(my_data);
}
