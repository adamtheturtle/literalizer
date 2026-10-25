#+feature dynamic-literals
package main

main :: proc() {
first := 3.5
my_data := first
my_data = first
_ = my_data
}
