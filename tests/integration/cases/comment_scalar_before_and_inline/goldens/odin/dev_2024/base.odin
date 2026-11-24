#+feature dynamic-literals
package main

main :: proc() {
// before
my_data := "plain"  // inline
_ = my_data
}
