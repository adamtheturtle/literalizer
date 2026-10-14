package main
func make_widget(args ...any) any { return nil }

func main() {
var my_data any = make_widget(nil)
my_data = make_widget(42) // note
// extra
}
