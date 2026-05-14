package main
func process(args ...any) any { return nil }

func main() {
process("hello", "a")
process(42, "b")
process(true, "c")
}
