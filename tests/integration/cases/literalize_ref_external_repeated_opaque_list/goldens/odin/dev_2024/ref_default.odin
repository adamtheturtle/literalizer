#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := [dynamic]any{}
my_data := [dynamic]any{
	item,
	item,
}
consume_widget(my_data);
}
