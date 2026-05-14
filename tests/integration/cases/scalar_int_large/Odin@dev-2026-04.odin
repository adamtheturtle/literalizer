#+feature dynamic-literals
package main

main :: proc() {
my_data := 2147483648
_ = my_data
}
