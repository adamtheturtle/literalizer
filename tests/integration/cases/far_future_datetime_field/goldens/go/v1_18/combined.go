package main
import "time"

func main() {
my_data := map[string]time.Time{
	"ts": time.Date(3000, time.December, 31, 23, 59, 59, 999999000, time.UTC),
}
my_data = map[string]time.Time{
	"ts": time.Date(3000, time.December, 31, 23, 59, 59, 999999000, time.UTC),
}
_ = my_data
}
