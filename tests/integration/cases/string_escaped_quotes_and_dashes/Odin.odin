#+feature dynamic-literals
package main

main :: proc() {
my_data := "hello \"world\" -- not a comment"
_ = my_data
}
