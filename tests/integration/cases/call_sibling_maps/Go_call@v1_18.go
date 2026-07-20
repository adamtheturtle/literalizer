package main
func process(args ...any) any { return nil }

func main() {
process(map[string]any{"value": 1})
process(map[string]any{"value": "hello"})
}
