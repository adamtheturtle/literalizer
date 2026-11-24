#+feature dynamic-literals
package main

main :: proc() {
first := true
my_data := first
my_data = first
_ = my_data
}
