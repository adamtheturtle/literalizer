package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := make_widget(42) // inner
 + 1
_ = my_data
}
