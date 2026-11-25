package main
import "time"

func main() {
my_data := map[string]time.Time{
	"within_i32": time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC),
	"beyond_i32": time.Date(2099, time.June, 15, 8, 30, 0, 0, time.UTC),
}
my_data = map[string]time.Time{
	"within_i32": time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC),
	"beyond_i32": time.Date(2099, time.June, 15, 8, 30, 0, 0, time.UTC),
}
_ = my_data
}
