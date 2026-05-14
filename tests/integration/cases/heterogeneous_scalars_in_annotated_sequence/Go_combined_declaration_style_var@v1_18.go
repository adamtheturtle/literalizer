package main
import "time"

func main() {
var my_data = []any{
	true,
	1.5,
	nil,
	time.Date(2020, time.January, 1, 0, 0, 0, 0, time.UTC),
	time.Date(2020, time.January, 1, 0, 0, 0, 0, time.UTC),
	[]any{},
}
my_data = []any{
	true,
	1.5,
	nil,
	time.Date(2020, time.January, 1, 0, 0, 0, 0, time.UTC),
	time.Date(2020, time.January, 1, 0, 0, 0, 0, time.UTC),
	[]any{},
}
_ = my_data
}
