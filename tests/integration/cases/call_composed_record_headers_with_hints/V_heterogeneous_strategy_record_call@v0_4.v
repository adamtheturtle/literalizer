struct Record0 {
	name string
	values []int
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := Record0{
		name: 'first',
		values: [
			1,
			2,
		],
	}
	consume(item);
}
