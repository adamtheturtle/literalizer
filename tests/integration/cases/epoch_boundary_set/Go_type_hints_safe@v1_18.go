package main
import "time"

func main() {
my_data := map[time.Time]struct{}{
	time.Date(1901, time.December, 13, 20, 45, 51, 0, time.UTC): struct{}{},
	time.Date(1901, time.December, 13, 20, 45, 52, 0, time.UTC): struct{}{},
	time.Date(2038, time.January, 19, 3, 14, 7, 0, time.UTC): struct{}{},
	time.Date(2038, time.January, 19, 3, 14, 8, 0, time.UTC): struct{}{},
}
_ = my_data
}
