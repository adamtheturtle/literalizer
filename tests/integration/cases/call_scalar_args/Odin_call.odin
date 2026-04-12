#+feature dynamic-literals
package main

main :: proc() {
process :: proc(_: ..any) {}
process("hello")
process(42)
process(true)
_ = my_data
}
