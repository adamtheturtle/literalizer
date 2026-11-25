#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
missing := [dynamic]any{
	1,
	2,
}
my_data := missing
consume_widget(my_data);
}
