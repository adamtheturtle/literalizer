package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := make_widget(42) ?
make_widget(42) // inner
: nil // trailing
_ = my_data
}
