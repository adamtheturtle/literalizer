#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := 42
my_data = make_widget(my_data) // note
make_widget(my_data);
}
