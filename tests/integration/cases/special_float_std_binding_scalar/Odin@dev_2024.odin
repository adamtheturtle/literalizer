#+feature dynamic-literals
package main
import "core:math"

main :: proc() {
std := math.nan_f64()
_ = std
}
