package main
import "core:math"

main :: proc() {
my_data := [dynamic]any{
	math.INF_F64,
	-math.INF_F64,
	math.NAN_F64,
}
_ = my_data
}
