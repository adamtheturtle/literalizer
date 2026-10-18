#+feature dynamic-literals
package main

main :: proc() {
my_null: any = nil
my_data := my_null
_ = my_data
}
