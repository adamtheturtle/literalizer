#+feature dynamic-literals
package main

main :: proc() {
my_data := 42
// after
_ = my_data
}
