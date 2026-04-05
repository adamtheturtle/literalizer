#+feature dynamic-literals
package main

main :: proc() {
my_data := "hello # world"  // note
_ = my_data
}
