#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(nil)
my_data = ($"{$"{1://}"}").Length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra
}
