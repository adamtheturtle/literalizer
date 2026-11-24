#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
shared := [dynamic]any{
	1,
	2,
}
my_data := [dynamic]any{
	0,
}
consume_widget(my_data);
my_data = shared
consume_widget(my_data);
}
