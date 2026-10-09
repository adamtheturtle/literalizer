package main
import "time"

func main() {
my_data := []map[string]time.Time{
	{"timestamp": time.Date(2020, time.January, 1, 0, 0, 0, 0, time.UTC)},
	{},
}
_ = my_data
}
