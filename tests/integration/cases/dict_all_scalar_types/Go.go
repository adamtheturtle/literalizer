package main
import "time"

func main() {
my_data := map[string]any{
	"s": "string",
	"i": 1,
	"f": 1.5,
	"b": true,
	"n": nil,
	"d": time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC),
	"dt": time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC),
	"by": "48656c6c6f",
}
_ = my_data
}
