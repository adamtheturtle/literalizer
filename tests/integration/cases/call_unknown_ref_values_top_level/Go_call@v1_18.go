package main
func process(args ...any) any { return nil }

func main() {
known_value := 1
unknown_value := []any{}
process(unknown_value)
}
