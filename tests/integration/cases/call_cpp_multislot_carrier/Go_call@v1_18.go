package main
func process(args ...any) any { return nil }

func main() {
process(1, "hello")
process("two", false)
process(3.5, nil)
}
