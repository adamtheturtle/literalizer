package main
import "time"

func main() {
my_data := map[time.Time]struct{}{
	time.Date(1969, time.December, 31, 23, 59, 59, 0, time.UTC): struct{}{},
}
_ = my_data
}
