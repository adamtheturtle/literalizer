interface IVal {}

fn main() {
	mut my_data := {
		'lint': [2, []IVal{}],
		'test': [5, ['compile']],
	}
	my_data = {
		'lint': [2, []IVal{}],
		'test': [5, ['compile']],
	}
	_ = my_data
}
