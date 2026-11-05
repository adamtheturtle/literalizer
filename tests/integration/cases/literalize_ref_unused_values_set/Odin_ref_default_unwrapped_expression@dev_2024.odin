#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
consume_widget(map[int]struct{}{
	1 = {},
	2 = {},
});
}
