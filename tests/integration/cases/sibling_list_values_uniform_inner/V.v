interface IVal {}

fn main() {
	my_data := {
		'lint': [IVal(2), IVal([1])],
		'test': [IVal(5), IVal([7])],
	}
	_ = my_data
}
