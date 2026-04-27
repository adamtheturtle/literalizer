interface IVal {}

fn main() {
	mut my_data := [
		IVal(1),
		IVal('hello'),
		IVal(true),
		IVal(unsafe { nil }),
	]
	_ = my_data
}
