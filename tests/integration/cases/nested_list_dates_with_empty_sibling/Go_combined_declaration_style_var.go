package main
import "time"

func main() {
var my_data = [][]time.Time{
	[]time.Time{time.Date(2026, time.January, 1, 0, 0, 0, 0, time.UTC), time.Date(2026, time.January, 2, 0, 0, 0, 0, time.UTC)},
	[]time.Time{},
	[]time.Time{time.Date(2026, time.February, 3, 0, 0, 0, 0, time.UTC), time.Date(2026, time.February, 4, 0, 0, 0, 0, time.UTC)},
}
my_data = [][]time.Time{
	[]time.Time{time.Date(2026, time.January, 1, 0, 0, 0, 0, time.UTC), time.Date(2026, time.January, 2, 0, 0, 0, 0, time.UTC)},
	[]time.Time{},
	[]time.Time{time.Date(2026, time.February, 3, 0, 0, 0, 0, time.UTC), time.Date(2026, time.February, 4, 0, 0, 0, 0, time.UTC)},
}
_ = my_data
}
