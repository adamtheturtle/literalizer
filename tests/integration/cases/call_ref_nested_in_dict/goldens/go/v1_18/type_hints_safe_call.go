package main
func process(args ...any) any { return nil }

func main() {
my_var := 42
process(map[string]any{"key": my_var, "count": 42, "label": "example"})
}
