package main
import "time"
type Record0 struct {
	S string
	I int
	F float64
	B bool
	N any
	D time.Time
	Dt int
	By string
}

func main() {
my_data := Record0{
	S: "string",
	I: 1,
	F: 1.5,
	B: true,
	N: nil,
	D: time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC),
	Dt: 1705320000,
	By: "48656c6c6f",
}
_ = my_data
}
