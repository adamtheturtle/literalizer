package main
func process(args ...any) any { return nil }
func emit(args ...any) any { return nil }

func main() {
emit(process("hello"), 1)
emit(process(42), 0)
}
