interface IVal {}

fn main() {
	mut my_data := [
		IVal(unsafe { nil }),
		IVal(unsafe { nil }),
	]
	my_data = [
		IVal(unsafe { nil }),
		IVal(unsafe { nil }),
	]
	_ = my_data
}
