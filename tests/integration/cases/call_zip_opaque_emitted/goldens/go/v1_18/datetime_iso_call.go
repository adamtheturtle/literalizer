package main
func process(args ...any) any { return nil }
func emit(args ...any) any { return nil }

func main() {
emit(process(1), "2024-01-15T12:00:00")
}
