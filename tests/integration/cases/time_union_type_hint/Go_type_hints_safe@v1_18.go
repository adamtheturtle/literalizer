package main
import "time"

func main() {
my_data := map[string][][]time.Time{
	"mixed": [][]time.Time{[]time.Time{time.Date(0, time.January, 1, 9, 30, 0, 0, time.UTC)}, []time.Time{}},
}
_ = my_data
}
