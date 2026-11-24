#+feature dynamic-literals
package main
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
item: any = nil
my_data: any = nil
consume_widget(my_data);
my_data = item
consume_widget(my_data);
}
