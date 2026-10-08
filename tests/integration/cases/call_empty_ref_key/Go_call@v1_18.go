package main
func consume(args ...any) any { return nil }

func main() {
external_value := 1
consume(external_value)
}
