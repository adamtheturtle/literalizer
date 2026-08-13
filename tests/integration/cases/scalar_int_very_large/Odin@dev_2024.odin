#+feature dynamic-literals
package main

main :: proc() {
my_data := u64(9223372036854775808)
_ = my_data
}
