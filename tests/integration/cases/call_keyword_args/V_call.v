interface IVal {}
interface ICallArg_ {}
struct throttlerType_ {}
fn (r throttlerType_) check(args ...ICallArg_) ICallArg_ { return 0 }
fn emit(args ...ICallArg_) {}

fn main() {
	throttler := throttlerType_{}
	emit(throttler.check('user_1', 1000.0));
	emit(throttler.check('user_2', 2000.5));
}
