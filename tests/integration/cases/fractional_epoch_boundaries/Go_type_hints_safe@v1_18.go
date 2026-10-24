package main
import "time"

func main() {
my_data := []time.Time{
	time.Date(1970, time.January, 1, 0, 0, 0, 1000, time.UTC),
	time.Date(1969, time.December, 31, 23, 59, 59, 500000000, time.UTC),
	time.Date(1970, time.January, 1, 0, 0, 1, 0, time.UTC),
}
_ = my_data
}
