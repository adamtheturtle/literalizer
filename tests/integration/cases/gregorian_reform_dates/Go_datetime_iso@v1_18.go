package main
import "time"

func main() {
my_data := map[string]any{
	"ancient_date": time.Date(1500, time.March, 1, 0, 0, 0, 0, time.UTC),
	"modern_date": time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC),
	"before_date": time.Date(1582, time.October, 4, 0, 0, 0, 0, time.UTC),
	"gap_date": time.Date(1582, time.October, 10, 0, 0, 0, 0, time.UTC),
	"transition_date": time.Date(1582, time.October, 15, 0, 0, 0, 0, time.UTC),
	"after_date": time.Date(1582, time.October, 16, 0, 0, 0, 0, time.UTC),
	"before_naive": "1582-10-04T12:30:00.000001",
	"gap_naive": "1582-10-10T12:30:00.500000",
	"transition_positive": "1582-10-15T00:30:00+18:00",
	"transition_negative": "1582-10-15T23:30:00-18:00",
	"after_positive": "1582-10-16T00:30:00+18:00",
}
_ = my_data
}
