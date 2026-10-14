package main
import "time"
func process(args ...any) any { return nil }
func emit(args ...any) any { return nil }

func main() {
emit(process(1), time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC))
}
