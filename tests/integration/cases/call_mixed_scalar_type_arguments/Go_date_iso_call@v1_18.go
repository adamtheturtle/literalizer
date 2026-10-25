package main
import "time"
import "math"
func capture(args ...any) any { return nil }

func main() {
capture(math.NaN(), math.Inf(1), math.Inf(-1), 1.25, "2024-01-15", time.Date(2024, time.January, 15, 12, 34, 56, 0, time.UTC), "[ordinary text]")
}
