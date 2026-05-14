#+feature dynamic-literals
package main

main :: proc() {
my_data := "hello # world"
_ = my_data
}
