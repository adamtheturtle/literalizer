package main
import "time"

func main() {
my_data := map[string]any{
	"date": "0099-05-27",
	"naive": time.Date(1, time.January, 1, 12, 30, 0, 0, time.UTC),
	"recent": time.Date(2024, time.May, 27, 10, 0, 0, 0, time.UTC),
}
_ = my_data
}
