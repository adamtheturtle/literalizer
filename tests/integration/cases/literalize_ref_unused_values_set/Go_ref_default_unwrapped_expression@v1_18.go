package main
func consume_widget(args ...any) any { return nil }

func main() {
consume_widget(map[int]struct{}{
	1: struct{}{},
	2: struct{}{},
})
}
