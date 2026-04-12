#+feature dynamic-literals
package main

main :: proc() {
process("hello")
process(42)
process(true)
_ = my_data
}
