package main
func consume(args ...any) any { return nil }

func main() {
Shared := 42
consume(Shared)
}
