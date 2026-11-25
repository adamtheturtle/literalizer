package main
func process(args ...any) any { return nil }

func main() {
process([]any{1, map[string]any{}}, 42)
}
