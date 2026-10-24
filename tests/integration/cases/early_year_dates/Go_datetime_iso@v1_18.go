package main
import "time"

func main() {
my_data := map[string]any{
	"date": time.Date(99, time.May, 27, 0, 0, 0, 0, time.UTC),
	"naive": "0001-01-01T12:30:00",
	"recent": "2024-05-27T10:00:00",
}
_ = my_data
}
