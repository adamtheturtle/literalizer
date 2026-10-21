#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
shared := [dynamic]any{
	1,
	2,
}
my_data := shared
consume_widget(my_data);
}
