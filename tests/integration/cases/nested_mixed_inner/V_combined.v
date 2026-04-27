interface IVal {}

fn main() {
	mut my_data := [
		[IVal(1), IVal('a')],
		[IVal(2), IVal('b')],
	]
	my_data = [
		[IVal(1), IVal('a')],
		[IVal(2), IVal('b')],
	]
	_ = my_data
}
