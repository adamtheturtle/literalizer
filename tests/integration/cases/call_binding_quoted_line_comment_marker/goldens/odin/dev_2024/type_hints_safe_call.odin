#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget("first \"quote\"\n// string body") // note
// extra
_ = my_data
}
