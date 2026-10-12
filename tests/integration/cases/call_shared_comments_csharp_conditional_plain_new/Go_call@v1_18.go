package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(42) : make_widget(42)
_ = my_data
}
