#+feature dynamic-literals
package main

main :: proc() {
my_data := map[any]struct{}{}
_ = my_data
}
