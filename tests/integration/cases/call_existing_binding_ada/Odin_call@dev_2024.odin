#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(0)
make_widget(my_data);
my_data = make_widget(1)
make_widget(my_data);
}
