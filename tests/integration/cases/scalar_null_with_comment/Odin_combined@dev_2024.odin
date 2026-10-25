#+feature dynamic-literals
package main

main :: proc() {
my_data: any = nil  // note
my_data = nil  // note
_ = my_data
}
