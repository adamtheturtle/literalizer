#+feature dynamic-literals
package main

main :: proc() {
record_data := [dynamic]any{}
my_data := record_data
_ = my_data
}
