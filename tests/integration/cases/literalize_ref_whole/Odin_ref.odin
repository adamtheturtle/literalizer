#+feature dynamic-literals
package main

main :: proc() {
my_var := 0
my_data := my_var
_ = my_data
}
