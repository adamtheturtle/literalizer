package main
import "time"

func main() {
my_data := []time.Time{
	time.Date(1901, time.December, 13, 20, 45, 51, 0, time.UTC),
	time.Date(1901, time.December, 13, 20, 45, 52, 0, time.UTC),
	time.Date(2038, time.January, 19, 3, 14, 7, 0, time.UTC),
	time.Date(2038, time.January, 19, 3, 14, 8, 0, time.UTC),
}
_ = my_data
}
