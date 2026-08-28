#+feature dynamic-literals
package main
record_entry :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := record_entry("a", 1, true)
_ = my_data
}
