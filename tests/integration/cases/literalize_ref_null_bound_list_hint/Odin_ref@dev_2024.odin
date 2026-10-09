#+feature dynamic-literals
package main

main :: proc() {
my_value: any = nil
my_data := my_value
_ = my_data
}
