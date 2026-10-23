package main
import "time"
func check(args ...any) any { return nil }

func main() {
check(time.Date(2024, time.January, 15, 10, 30, 0, 0, time.UTC), time.Date(2024, time.June, 1, 0, 0, 0, 0, time.UTC))
}
