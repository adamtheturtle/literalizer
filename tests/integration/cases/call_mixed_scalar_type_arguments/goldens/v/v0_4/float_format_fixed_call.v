import math
interface ICallArg_ {}
fn capture(args ...ICallArg_) {}

fn main() {
	capture(math.nan(), math.inf(1), math.inf(-1), 1.250000, "2024-01-15", "2024-01-15T12:34:56", '[ordinary text]');
}
