#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := [dynamic]any{
	1,
	2,
}
my_data := [dynamic]any{
	1,
	2,
}
consume_widget(my_data);
my_data = item
consume_widget(my_data);
}
