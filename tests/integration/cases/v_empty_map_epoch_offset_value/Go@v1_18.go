package main
import "time"

func main() {
my_data := []map[string]time.Time{
	{"timestamp": time.Date(2040, time.January, 1, 3, 0, 0, 0, time.FixedZone("", 10800))},
	{},
}
_ = my_data
}
