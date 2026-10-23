#+feature dynamic-literals
package main

main :: proc() {
my_data := 0x2a
// after
_ = my_data
}
