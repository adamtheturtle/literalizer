#+feature dynamic-literals
package main
Record0 :: struct { a: int, b: string }
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
consume_widget(Record0{
	a = 1,
	b = "x",
});
}
