#+feature dynamic-literals
package main

main :: proc() {
first := 42
my_data := first
_ = my_data
}
