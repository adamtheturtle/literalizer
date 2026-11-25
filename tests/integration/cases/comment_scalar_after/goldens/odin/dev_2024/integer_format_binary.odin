#+feature dynamic-literals
package main

main :: proc() {
my_data := 0b101010
// after
_ = my_data
}
