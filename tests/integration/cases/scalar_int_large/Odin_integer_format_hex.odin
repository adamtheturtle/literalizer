#+feature dynamic-literals
package main

main :: proc() {
my_data := 0x80000000
_ = my_data
}
