package main
import "math"
type Record0 struct {
	Nan float64
	Positive float64
	Negative float64
}

func main() {
std := Record0{
	Nan: math.NaN(),
	Positive: math.Inf(1),
	Negative: math.Inf(-1),
}
_ = std
}
