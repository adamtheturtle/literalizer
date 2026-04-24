package main
func process(args ...any) any { return nil }

func main() {
items := []any{
	process(1, 42),
	process(2, 100),
}
_ = items
}
