package main
func consume(args ...any) any { return nil }

func main() {
item := 42
consume(map[string]int{"field": item})
}
