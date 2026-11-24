struct Record0 {
	value int
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := Record0{
		value: 1,
	}
	consume(item);
}
