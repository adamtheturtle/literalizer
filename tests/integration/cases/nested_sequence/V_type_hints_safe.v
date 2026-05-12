interface IVal {}

fn main() {
	my_data := [
		IVal(true),
		IVal('hi'),
		IVal([1, 2]),
		IVal(unsafe { nil }),
	]
	_ = my_data
}
