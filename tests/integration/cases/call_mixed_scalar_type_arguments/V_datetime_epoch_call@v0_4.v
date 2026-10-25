import math
interface ICallArg_ {}
fn capture(args ...ICallArg_) {}

fn main() {
	capture(math.nan(), math.inf(1), math.inf(-1), 1.25, "2024-01-15", 1705322096, '[ordinary text]');
}
