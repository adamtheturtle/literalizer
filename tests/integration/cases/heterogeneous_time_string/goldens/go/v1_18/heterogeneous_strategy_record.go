package main
import "time"
type Record0 struct {
	Vals []any
}

func main() {
my_data := Record0{
	Vals: []any{
		time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC),
		"hello",
	},
}
_ = my_data
}
