package main
import "time"
func process(args ...any) any { return nil }

func main() {
process(time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC))
process(time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC))
process(1)
}
