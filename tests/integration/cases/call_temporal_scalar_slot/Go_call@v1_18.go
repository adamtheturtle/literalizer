package main
import "time"
func process(args ...any) any { return nil }

func main() {
process("09:30:00")
process(time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC))
process(1)
}
