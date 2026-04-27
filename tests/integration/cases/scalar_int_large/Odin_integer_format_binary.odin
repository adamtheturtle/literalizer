#+feature dynamic-literals
package main

main :: proc() {
my_data := 0b10000000000000000000000000000000
_ = my_data
}
