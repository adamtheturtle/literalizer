package main
import "time"

func main() {
my_data := []map[string]any{
	{"k": time.Date(2040, time.January, 1, 0, 0, 0, 0, time.UTC)},
	{"k": 1},
}
_ = my_data
}
