#+feature dynamic-literals
package main

main :: proc() {
my_data: any = nil
my_data = nil
_ = my_data
}
