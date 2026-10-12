#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := $"{$"{1://}"}" // trailing
// extra
_ = my_data
}
