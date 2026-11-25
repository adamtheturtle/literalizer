package main
import "time"

func main() {
my_data := []map[string]map[string][]time.Time{
	{"nested": map[string][]time.Time{"times": []time.Time{time.Date(1900, time.January, 1, 0, 0, 0, 0, time.UTC)}}},
	{},
}
_ = my_data
}
