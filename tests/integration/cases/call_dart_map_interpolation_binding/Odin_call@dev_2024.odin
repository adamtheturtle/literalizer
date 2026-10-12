#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := "${{'value': '// payload'}['value']}" // trailing
// extra
_ = my_data
}
