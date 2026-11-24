package main
import "time"

func main() {
my_data := map[string][]time.Time{
	"times": []time.Time{time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC), time.Date(0, time.January, 1, 17, 45, 0, 0, time.UTC), time.Date(0, time.January, 1, 23, 59, 59, 0, time.UTC)},
}
my_data = map[string][]time.Time{
	"times": []time.Time{time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC), time.Date(0, time.January, 1, 17, 45, 0, 0, time.UTC), time.Date(0, time.January, 1, 23, 59, 59, 0, time.UTC)},
}
_ = my_data
}
