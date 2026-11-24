package main
import "time"

func main() {
my_data := map[string]any{
	"vals": []any{time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC), time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC)},
}
_ = my_data
}
