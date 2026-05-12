package main
import "time"

func main() {
my_data := map[string]any{
	"name": "Alice",
	"age": 30,
	"active": true,
	"score": nil,
	"joined": time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC),
	"last_login": time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC),
	"avatar": "48656c6c6f",
}
_ = my_data
}
