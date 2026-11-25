#+feature dynamic-literals
package main

main :: proc() {
my_data := 0o52  // note
_ = my_data
}
