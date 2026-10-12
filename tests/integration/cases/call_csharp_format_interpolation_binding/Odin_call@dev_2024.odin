#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := $"{{payload}} {1://}" // trailing
// extra
_ = my_data
}
