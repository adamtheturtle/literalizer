#+feature dynamic-literals
package main
import "core:math"
capture :: proc(args: ..any) -> any { return nil }

main :: proc() {
capture(math.nan_f64(), math.inf_f64(1), math.inf_f64(-1), 1.250000, "2024-01-15", "2024-01-15T12:34:56", "[ordinary text]");
}
