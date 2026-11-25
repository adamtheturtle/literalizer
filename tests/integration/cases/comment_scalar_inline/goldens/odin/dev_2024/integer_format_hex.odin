#+feature dynamic-literals
package main

main :: proc() {
my_data := 0x2a  // note
_ = my_data
}
