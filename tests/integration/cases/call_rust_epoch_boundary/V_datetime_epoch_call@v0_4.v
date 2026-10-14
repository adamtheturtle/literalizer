interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	consume(i64(-2147483649));
	consume(i64(2147483648));
}
