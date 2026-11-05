package main
func process(args ...any) any { return nil }
func emit(args ...any) any { return nil }

func main() {
emit(process("hello"), map[string]int{"a": 1, "b": 2})
emit(process(42), map[string]int{"c": 3, "d": 4})
}
