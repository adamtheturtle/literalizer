package main
import "time"

func main() {
MyTime := time.Date(0, time.January, 1, 1, 2, 3, 0, time.UTC)
my_data := map[string]time.Time{
	"x": MyTime,
}
_ = my_data
}
