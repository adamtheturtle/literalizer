package main
import "time"

func main() {
my_data := map[time.Time]struct{}{
	time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC): struct{}{},
	time.Date(2024, time.June, 1, 0, 0, 0, 0, time.UTC): struct{}{},
}
_ = my_data
}
