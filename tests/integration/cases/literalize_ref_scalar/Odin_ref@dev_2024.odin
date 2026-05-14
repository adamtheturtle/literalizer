#+feature dynamic-literals
package main

main :: proc() {
my_int := 42
my_data := my_int
_ = my_data
}
