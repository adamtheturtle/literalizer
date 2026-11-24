package main
import "time"
type Record0 struct {
	A int
}
func consume(args ...any) any { return nil }

func main() {
stamp := time.Date(2001, time.February, 3, 0, 0, 0, 0, time.UTC)
item := Record0{
	A: 1,
}
consume(stamp, item)
}
