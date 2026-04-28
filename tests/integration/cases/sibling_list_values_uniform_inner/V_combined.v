interface IVal {}

fn main() {
	mut my_data := {
		'lint': [IVal(2), IVal([1])],
		'test': [IVal(5), IVal([7])],
	}
	my_data = {
		'lint': [IVal(2), IVal([1])],
		'test': [IVal(5), IVal([7])],
	}
	_ = my_data
}
