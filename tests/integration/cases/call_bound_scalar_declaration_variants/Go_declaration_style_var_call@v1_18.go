package main
func consume(args ...any) any { return nil }

func main() {
var Shared = 42
consume(Shared)
}
