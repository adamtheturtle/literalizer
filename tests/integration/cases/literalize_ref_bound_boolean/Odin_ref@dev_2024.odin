#+feature dynamic-literals
package main

main :: proc() {
ref_flag := true
my_data := ref_flag
_ = my_data
}
