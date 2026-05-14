interface IVal {}
interface ICallArg_ {}
struct ThrottlerType_ {}
fn (r ThrottlerType_) check(args ...ICallArg_) {}

fn main() {
	throttler := ThrottlerType_{}
	throttler.check();
	throttler.check();
}
