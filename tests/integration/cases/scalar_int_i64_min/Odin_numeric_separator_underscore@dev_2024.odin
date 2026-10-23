#+feature dynamic-literals
package main

main :: proc() {
my_data := -9_223_372_036_854_775_808
_ = my_data
}
