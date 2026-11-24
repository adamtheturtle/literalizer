struct Record0 {
	a int
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	stamp := "2001-02-03"
	item := Record0{
		a: 1,
	}
	consume(stamp, item);
}
