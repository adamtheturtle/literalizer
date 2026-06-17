package main
func record_value(args ...any) any { return nil }
func flush_buffer(args ...any) any { return nil }
func emit(args ...any) any { return nil }

func main() {
emit(record_value(42))
flush_buffer(3)
}
