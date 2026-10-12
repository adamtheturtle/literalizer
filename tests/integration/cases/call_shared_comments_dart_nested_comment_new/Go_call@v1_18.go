package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := ("${"${"// payload"}"}").length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra
_ = my_data
}
