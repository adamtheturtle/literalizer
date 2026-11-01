struct Record0 {
	a int
	b string
}
interface ICallArg_ {}
fn consume_widget(args ...ICallArg_) {}

fn main() {
	consume_widget(Record0{
		a: 1,
		b: 'x',
	});
}
