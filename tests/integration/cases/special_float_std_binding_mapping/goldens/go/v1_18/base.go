package main
import "math"

func main() {
std := map[string]float64{
	"nan": math.NaN(),
	"positive": math.Inf(1),
	"negative": math.Inf(-1),
}
_ = std
}
