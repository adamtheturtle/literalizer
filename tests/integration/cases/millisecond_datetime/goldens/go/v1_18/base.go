package main
import "time"

func main() {
my_data := map[string]time.Time{
	"half": time.Date(1979, time.May, 27, 7, 32, 0, 500000000, time.UTC),
	"milli": time.Date(1979, time.May, 27, 7, 32, 0, 100000000, time.UTC),
	"max_milli": time.Date(1979, time.May, 27, 7, 32, 0, 999000000, time.UTC),
	"whole": time.Date(1979, time.May, 27, 7, 32, 0, 0, time.UTC),
}
_ = my_data
}
