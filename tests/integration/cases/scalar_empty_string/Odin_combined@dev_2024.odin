#+feature dynamic-literals
package main

main :: proc() {
my_data := ""
my_data = ""
_ = my_data
}
