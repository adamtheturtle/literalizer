#+feature dynamic-literals
package main
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_null: any = nil
regular_null: any = nil
consume(my_null);
consume(regular_null);
}
