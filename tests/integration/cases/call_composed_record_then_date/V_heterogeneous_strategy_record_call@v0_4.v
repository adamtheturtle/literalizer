struct Record0 {
	a int
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := Record0{
		a: 1,
	}
	stamp := "2001-02-03"
	consume(stamp, item);
}
