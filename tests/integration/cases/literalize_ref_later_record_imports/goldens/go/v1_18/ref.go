package main
import "time"
type Record1 struct {
	X int
}
type Record2 struct {
	Day time.Time
	Stamp time.Time
}
type Record0 struct {
	Plain Record1
	Timed Record2
}

func main() {
Plain := Record1{
	X: 1,
}
Timed := Record2{
	Day: time.Date(2001, time.January, 2, 0, 0, 0, 0, time.UTC),
	Stamp: time.Date(2001, time.January, 2, 3, 4, 5, 0, time.UTC),
}
my_data := Record0{
	Plain: Plain,
	Timed: Timed,
}
_ = my_data
}
