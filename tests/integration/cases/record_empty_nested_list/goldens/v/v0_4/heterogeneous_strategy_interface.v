interface IVal {}

fn main() {
	my_data := {
		'a': IVal([[1, 2], [3]]),
		'b': IVal([IVal([]int{}), IVal([1])]),
	}
	_ = my_data
}
