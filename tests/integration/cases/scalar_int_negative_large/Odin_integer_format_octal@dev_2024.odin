#+feature dynamic-literals
package main

main :: proc() {
my_data := -0o20000000001
_ = my_data
}
