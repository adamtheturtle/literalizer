#+feature dynamic-literals
package main

main :: proc() {
my_data := "\nroot first line\n  indented\n\nroot last line\n"
_ = my_data
}
