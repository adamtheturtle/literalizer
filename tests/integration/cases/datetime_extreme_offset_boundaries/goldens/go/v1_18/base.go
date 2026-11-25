package main
import "time"

func main() {
my_data := []time.Time{
	time.Date(2020, time.June, 15, 12, 0, 0, 0, time.FixedZone("", -86340)),
	time.Date(2020, time.June, 15, 12, 0, 0, 0, time.FixedZone("", -64800)),
	time.Date(2020, time.June, 15, 12, 0, 0, 0, time.FixedZone("", 64800)),
	time.Date(2020, time.June, 15, 12, 0, 0, 0, time.FixedZone("", 86340)),
}
_ = my_data
}
