package main
import "time"

func main() {
my_data := map[string]any{
	"date": time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC),
	"datetime": time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC),
}
_ = my_data
}
