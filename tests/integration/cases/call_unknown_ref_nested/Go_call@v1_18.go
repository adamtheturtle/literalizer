package main
func process(args ...any) any { return nil }

func main() {
known_value := true
unknown_value := true
process(known_value, unknown_value)
}
