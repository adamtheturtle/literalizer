#+feature dynamic-literals
package main
store_item :: proc(args: ..any) -> any { return nil }
read_item :: proc(args: ..any) -> any { return nil }

main :: proc() {
store_item(1, 10);
read_item(1);
}
