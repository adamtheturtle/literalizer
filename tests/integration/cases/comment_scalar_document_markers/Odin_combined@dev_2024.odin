#+feature dynamic-literals
package main

main :: proc() {
// note
my_data := 42
// note
my_data = 42
_ = my_data
}
