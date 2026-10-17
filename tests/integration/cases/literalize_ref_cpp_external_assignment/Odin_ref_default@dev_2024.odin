#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
ref_data := [dynamic]any{
	1,
	2,
}
my_data := [dynamic]any{
	0,
}
consume_widget(my_data);
my_data = ref_data
consume_widget(my_data);
}
