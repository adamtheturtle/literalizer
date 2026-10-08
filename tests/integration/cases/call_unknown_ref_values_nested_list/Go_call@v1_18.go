package main
func process(args ...any) any { return nil }

func main() {
unknown_value := []any{}
process([]map[string]string{unknown_value})
}
