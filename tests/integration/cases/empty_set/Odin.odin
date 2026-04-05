#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]struct{}{}
_ = my_data
}
