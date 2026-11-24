package main
import "time"

func main() {
my_data := []time.Time{
	time.Date(2024, time.January, 15, 12, 30, 0, 123456000, time.UTC),
	time.Date(2024, time.June, 1, 8, 0, 0, 0, time.UTC),
}
_ = my_data
}
