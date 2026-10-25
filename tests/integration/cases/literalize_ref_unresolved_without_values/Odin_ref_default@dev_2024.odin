#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
a := 0
my_data := [dynamic]any{
	a,
	1,
}
consume_widget(my_data);
}
