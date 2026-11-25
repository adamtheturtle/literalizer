#+feature dynamic-literals
package main
import "core:math"

main :: proc() {
my_data := [dynamic]any{
	math.inf_f64(1),
	math.inf_f64(-1),
	math.nan_f64(),
}
_ = my_data
}
