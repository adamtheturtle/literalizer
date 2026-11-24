#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
shared := 1
my_data := shared
consume_widget(my_data);
}
