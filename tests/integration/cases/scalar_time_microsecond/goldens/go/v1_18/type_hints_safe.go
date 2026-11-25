package main
import "time"

func main() {
my_data := map[string]time.Time{
	"exact_millisecond": time.Date(0, time.January, 1, 9, 30, 15, 123000000, time.UTC),
	"sub_millisecond": time.Date(0, time.January, 1, 9, 30, 15, 123456000, time.UTC),
}
_ = my_data
}
