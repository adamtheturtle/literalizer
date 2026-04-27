interface IVal {}

fn main() {
	mut my_data := [
		[IVal(1), IVal(2)],
		[]IVal{},
		[IVal('a'), IVal('b')],
	]
	my_data = [
		[IVal(1), IVal(2)],
		[]IVal{},
		[IVal('a'), IVal('b')],
	]
	_ = my_data
}
