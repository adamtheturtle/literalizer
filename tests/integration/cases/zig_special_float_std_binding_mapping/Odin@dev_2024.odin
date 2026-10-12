#+feature dynamic-literals
package main
import "core:math"

main :: proc() {
std := map[string]any{
	"nan" = math.nan_f64(),
	"positive" = math.inf_f64(1),
	"negative" = math.inf_f64(-1),
}
_ = std
}
