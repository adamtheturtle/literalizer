interface IVal {}

fn main() {
	my_data := [
		[IVal(1), IVal('value')],
		[]IVal{},
	]
	_ = my_data
}
