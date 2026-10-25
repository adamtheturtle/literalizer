#+feature dynamic-literals
package main

main :: proc() {
my_data := 3.14
my_data = 3.14
_ = my_data
}
