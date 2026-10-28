package main
import "time"

func main() {
my_data := map[string]any{
	"before_date": "1582-10-04",
	"gap_date": "1582-10-10",
	"transition_date": "1582-10-15",
	"after_date": "1582-10-16",
	"before_naive": time.Date(1582, time.October, 4, 12, 30, 0, 1000, time.UTC),
	"gap_naive": time.Date(1582, time.October, 10, 12, 30, 0, 500000000, time.UTC),
	"transition_positive": time.Date(1582, time.October, 15, 0, 30, 0, 0, time.FixedZone("", 64800)),
	"transition_negative": time.Date(1582, time.October, 15, 23, 30, 0, 0, time.FixedZone("", -64800)),
	"after_positive": time.Date(1582, time.October, 16, 0, 30, 0, 0, time.FixedZone("", 64800)),
}
_ = my_data
}
