#+feature dynamic-literals
package main

main :: proc() {
my_data := "\x00x"
_ = my_data
}
