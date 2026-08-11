package main
import "time"

func main() {
my_data := map[string]time.Time{
	"starts_at": time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC),
}
_ = my_data
}
