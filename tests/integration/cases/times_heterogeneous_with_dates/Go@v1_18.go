package main
import "time"

func main() {
my_data := map[string]any{
	"vals": []any{time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC), "09:30:00"},
}
_ = my_data
}
