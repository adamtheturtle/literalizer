struct Record0 {
	a int
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := Record0{
		a: 1,
	}
	consume(item);
}
