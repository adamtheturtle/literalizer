package main
import "time"

func main() {
my_data := map[time.Time]struct{}{
	time.Date(2099, time.June, 15, 8, 30, 0, 0, time.UTC): struct{}{},
}
_ = my_data
}
