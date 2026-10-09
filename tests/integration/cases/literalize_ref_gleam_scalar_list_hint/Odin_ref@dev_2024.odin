#+feature dynamic-literals
package main

main :: proc() {
ref_data := 1
my_data := ref_data
_ = my_data
}
