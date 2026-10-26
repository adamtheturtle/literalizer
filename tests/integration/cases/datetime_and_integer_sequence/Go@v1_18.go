package main
import "time"

func main() {
my_data := []any{
	time.Date(2000, time.January, 1, 1, 2, 3, 0, time.UTC),
	1,
}
_ = my_data
}
