package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := make_widget(`first "quote"
// string body`) // note
// extra
_ = my_data
}
