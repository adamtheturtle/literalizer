interface IVal {}
interface ICallArg_ {}
struct ThrottlerType_ {}
fn (r ThrottlerType_) check() {}

fn main() {
	throttler := ThrottlerType_{}
	throttler.check();
	throttler.check();
}
