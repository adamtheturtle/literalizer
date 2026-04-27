#+feature dynamic-literals
package main

main :: proc() {
my_data := 2_147_483_648
_ = my_data
}
