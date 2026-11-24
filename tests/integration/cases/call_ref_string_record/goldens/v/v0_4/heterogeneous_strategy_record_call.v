struct Record0 {
	value string
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := Record0{
		value: 'owned',
	}
	consume(item);
}
