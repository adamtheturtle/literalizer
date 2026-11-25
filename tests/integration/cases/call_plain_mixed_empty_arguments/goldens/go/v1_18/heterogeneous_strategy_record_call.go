package main
func make_widget(args ...any) any { return nil }

func main() {
make_widget([]any{}, []int{1}, []any{})
make_widget([]string{"text"}, []int{2}, []any{})
make_widget([]any{}, []string{"text"}, []any{})
make_widget([]string{"text"}, []int{2}, []int{3})
}
