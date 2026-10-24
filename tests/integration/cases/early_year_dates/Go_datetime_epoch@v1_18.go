package main
import "time"

func main() {
my_data := map[string]any{
	"date": time.Date(99, time.May, 27, 0, 0, 0, 0, time.UTC),
	"naive": -62135551800,
	"recent": 1716804000,
}
_ = my_data
}
