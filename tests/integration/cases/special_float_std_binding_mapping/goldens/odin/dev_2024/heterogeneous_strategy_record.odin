#+feature dynamic-literals
package main
import "core:math"
Record0 :: struct { nan: f64, positive: f64, negative: f64 }

main :: proc() {
std := Record0{
	nan = math.nan_f64(),
	positive = math.inf_f64(1),
	negative = math.inf_f64(-1),
}
_ = std
}
