package main
func process(args ...any) any { return nil }
func emit(args ...any) any { return nil }

func main() {
emit(process("hello"), "one")
emit(process(42), "zero")
}
