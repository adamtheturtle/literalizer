package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := "${"${"// payload"}"}" // trailing
// extra
_ = my_data
}
