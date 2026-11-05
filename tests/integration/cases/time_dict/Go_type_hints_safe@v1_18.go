package main
import "time"

func main() {
my_data := map[string]time.Time{
	"morning": time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC),
	"afternoon": time.Date(0, time.January, 1, 14, 15, 0, 0, time.UTC),
	"evening": time.Date(0, time.January, 1, 23, 59, 59, 0, time.UTC),
}
_ = my_data
}
