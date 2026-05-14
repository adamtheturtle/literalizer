#+feature dynamic-literals
package main

main :: proc() {
my_data := map[int]struct{}{}
_ = my_data
}
