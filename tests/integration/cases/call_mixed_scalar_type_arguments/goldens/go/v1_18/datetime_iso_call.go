package main
import "time"
import "math"
func capture(args ...any) any { return nil }

func main() {
capture(math.NaN(), math.Inf(1), math.Inf(-1), 1.25, time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC), "2024-01-15T12:34:56", "[ordinary text]")
}
